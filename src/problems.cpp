#include "problems.hpp"
#include "apierror.hpp"
#include "compiler.hpp"
#include "problemjudge.hpp"
#include "submitstore.hpp"
#include "ziputil.hpp"
#include "testlib_asset.hpp"
#include <algorithm>
#include <cstdio>
#include <map>
#include <set>
#include <string_view>

namespace {
const std::set<std::string> kFields={"schemaVersion","id","title","difficulty","tags","limits","judgeMode","statement",
    "hints","samples","groups","function","checker","solution","tests","testsZipPath","notes"};
// 规格 §4.5：标签只能取这张表，出题模型不许自由发挥。
const std::set<std::string> kTags={"模拟","枚举","排序","二分","贪心","构造","前缀和","差分","双指针","滑动窗口","哈希","栈",
    "队列","单调栈","堆","并查集","树状数组","线段树","字符串","Trie","KMP","图论","最短路","最小生成树","拓扑排序","二分图",
    "网络流","树","最近公共祖先","动态规划","背包","区间DP","状压DP","数位DP","树形DP","数学","数论","组合数学","概率期望",
    "计算几何","位运算","分治","记忆化搜索","高精度","交互"};

struct Structure {
    std::string id,checker,zipPath;
    Json meta;
    std::vector<ProblemCase> cases; // 只有 tests 内嵌时有意义
    std::vector<std::string> drivers,solutions;
    bool hasTests=false,functionMode=false;
};
struct Issues {
    std::vector<Json> details;
    void error(std::string message) { details.push_back({{"level","error"},{"message",std::move(message)}}); }
    bool empty() const { return details.empty(); }
};
struct Workspace {
    fs::path path;
    explicit Workspace(const fs::path& base) : path(base) { fs::create_directories(path); }
    Workspace(const Workspace&)=delete;
    ~Workspace() { std::error_code error; fs::remove_all(path,error); }
};
std::string trim(const std::string& text) {
    auto first=text.find_first_not_of(" \t\r\n");
    if(first==std::string::npos) return {};
    auto last=text.find_last_not_of(" \t\r\n");
    return text.substr(first,last-first+1);
}
std::string stripBom(std::string text) {
    if(text.size()>=3 && static_cast<unsigned char>(text[0])==0xEF && static_cast<unsigned char>(text[1])==0xBB && static_cast<unsigned char>(text[2])==0xBF)
        text.erase(0,3);
    return text;
}
std::size_t textWidth(const std::string& text) {
    std::size_t count=0;
    for(unsigned char c:text) if((c&0xC0)!=0x80) ++count;
    return count;
}
bool lower(char c) { return c>='a' && c<='z'; }
bool digit(char c) { return c>='0' && c<='9'; }
bool validId(const std::string& id) {
    if(id.size()<2 || id.size()>48 || (!lower(id[0]) && !digit(id[0]))) return false;
    for(char c:id) if(!lower(c) && !digit(c) && c!='-') return false;
    return true;
}
bool validCaseId(const std::string& id) {
    if(id.empty() || id.size()>16 || (!lower(id[0]) && !digit(id[0]))) return false;
    for(char c:id) if(!lower(c) && !digit(c) && c!='-' && c!='_') return false;
    return true;
}
bool validGroupName(const std::string& name) {
    if(name.empty() || name.size()>16 || !lower(name[0])) return false;
    for(char c:name) if(!lower(c) && !digit(c) && c!='-' && c!='_') return false;
    return true;
}
bool stringAt(const Json& object,const char* key,std::string& value) {
    if(!object.contains(key) || !object.at(key).is_string()) return false;
    value=object.at(key).get<std::string>(); return true;
}
bool integerAt(const Json& object,const char* key,long long& value) {
    if(!object.contains(key) || !object.at(key).is_number_integer()) return false;
    value=object.at(key).get<long long>(); return true;
}
std::string nowIso() {
    SYSTEMTIME now; GetSystemTime(&now);
    char buffer[64];
    std::snprintf(buffer,sizeof(buffer),"%04d-%02d-%02dT%02d:%02d:%02dZ",now.wYear,now.wMonth,now.wDay,now.wHour,now.wMinute,now.wSecond);
    return buffer;
}
std::string firstLines(const std::string& log,std::size_t maxLines) {
    std::string result; std::size_t start=0,lines=0;
    while(start<log.size() && lines<maxLines) {
        auto end=log.find('\n',start);
        if(end==std::string::npos) end=log.size();
        result+=log.substr(start,end-start);
        result+='\n'; ++lines; start=end+1;
    }
    if(result.size()>8000) result.resize(8000);
    return result;
}
std::vector<std::string> unitsOf(const Json& value) {
    std::vector<std::string> units;
    if(value.is_string()) units.push_back(value.get<std::string>());
    else if(value.is_array()) for(const auto& item:value) units.push_back(item.get<std::string>());
    return units;
}
void mergeDetails(const Issues& issues,const std::string& message) {
    throw ApiError(400,message,{{"details",issues.details}});
}

// ---- 1–5：结构校验（纯内存，不编译） ----
void validateDocument(const Json& document,Structure& structure,Issues& issues) {
    auto error=[&](std::string message) { issues.error(std::move(message)); };
    if(!document.is_object()) { error("problem.json 顶层必须是 JSON 对象"); return; }
    for(auto it=document.begin();it!=document.end();++it)
        if(!kFields.contains(it.key())) error("未知字段 "+it.key());
    structure.meta=document;

    long long version=0;
    if(!integerAt(document,"schemaVersion",version) || version!=1) error("schemaVersion 必须为 1");

    std::string id;
    if(!stringAt(document,"id",id)) error("id 缺失或不是字符串");
    else if(!validId(id)) error("id 格式不合法：需匹配 ^[a-z0-9][a-z0-9-]{1,47}$");
    else structure.id=id;

    if(!document.contains("title") || !document.at("title").is_object()) error("title 缺失或不是对象");
    else {
        const auto& title=document.at("title");
        for(auto it=title.begin();it!=title.end();++it)
            if(it.key()!="zh" && it.key()!="en") error("title 含有未知字段 "+it.key());
        for(const auto* key:{"zh","en"}) {
            std::string text;
            if(!stringAt(title,key,text) || trim(text).empty()) error(std::string("title.")+key+" 不能为空");
            else if(textWidth(text)>80) error(std::string("title.")+key+" 超过 80 个字符");
        }
    }
    long long difficulty=0;
    if(!integerAt(document,"difficulty",difficulty)) error("difficulty 缺失或不是整数");
    else if(difficulty<800 || difficulty>3500 || difficulty%100) error("difficulty 必须是 800–3500 之间 100 的整数倍");

    if(!document.contains("tags") || !document.at("tags").is_array()) error("tags 缺失或不是数组");
    else {
        const auto& tags=document.at("tags");
        if(tags.empty() || tags.size()>3) error("tags 需要 1–3 个");
        for(std::size_t i=0;i<tags.size();++i) {
            if(!tags[i].is_string()) { error("tags["+std::to_string(i)+"] 必须是字符串"); continue; }
            auto tag=tags[i].get<std::string>();
            if(!kTags.contains(tag)) error("未知标签 "+tag);
        }
    }
    if(!document.contains("limits") || !document.at("limits").is_object()) error("limits 缺失或不是对象");
    else {
        const auto& limits=document.at("limits");
        for(auto it=limits.begin();it!=limits.end();++it)
            if(it.key()!="timeMs" && it.key()!="memoryMb") error("limits 含有未知字段 "+it.key());
        long long timeMs=0,memoryMb=0;
        if(!integerAt(limits,"timeMs",timeMs)) error("limits.timeMs 缺失或不是整数");
        else if(timeMs<100 || timeMs>60000) error("limits.timeMs 超出范围 100..60000");
        if(!integerAt(limits,"memoryMb",memoryMb)) error("limits.memoryMb 缺失或不是整数");
        else if(memoryMb<16 || memoryMb>4096) error("limits.memoryMb 超出范围 16..4096");
    }
    std::string mode;
    if(!stringAt(document,"judgeMode",mode)) error("judgeMode 缺失或不是字符串");
    else if(mode!="io" && mode!="function") error("judgeMode 只能是 io 或 function");
    else structure.functionMode=mode=="function";

    if(!document.contains("statement") || !document.at("statement").is_object()) error("statement 缺失或不是对象");
    else {
        const auto& statement=document.at("statement");
        for(auto it=statement.begin();it!=statement.end();++it)
            if(it.key()!="zh" && it.key()!="en") error("statement 含有未知字段 "+it.key());
        for(const auto* key:{"zh","en"}) {
            std::string text;
            if(!stringAt(statement,key,text) || trim(text).empty()) error(std::string("statement.")+key+" 不能为空");
            else if(text.size()>64*1024) error(std::string("statement.")+key+" 超过 64 KB");
        }
    }
    if(document.contains("hints")) {
        if(!document.at("hints").is_object()) error("hints 必须是对象");
        else {
            const auto& hints=document.at("hints");
            for(auto it=hints.begin();it!=hints.end();++it)
                if(it.key()!="zh" && it.key()!="en") error("hints 含有未知字段 "+it.key());
            for(const auto* key:{"zh","en"}) {
                if(!hints.contains(key)) continue;
                const auto& list=hints.at(key);
                if(!list.is_array()) { error(std::string("hints.")+key+" 必须是数组"); continue; }
                if(list.size()>4) error(std::string("hints.")+key+" 最多 4 条");
                for(std::size_t i=0;i<list.size();++i) {
                    if(!list[i].is_string()) { error("hints."+std::string(key)+"["+std::to_string(i)+"] 必须是字符串"); continue; }
                    if(textWidth(list[i].get<std::string>())>300) error("hints."+std::string(key)+" 第 "+std::to_string(i+1)+" 条超过 300 字");
                }
            }
        }
    }
    if(!document.contains("samples") || !document.at("samples").is_array()) error("samples 缺失或不是数组");
    else {
        const auto& samples=document.at("samples");
        if(samples.empty() || samples.size()>5) error("samples 需要 1–5 项");
        for(std::size_t i=0;i<samples.size();++i) {
            const auto& item=samples[i];
            auto label="samples["+std::to_string(i)+"]";
            if(!item.is_object()) { error(label+" 必须是对象"); continue; }
            for(auto it=item.begin();it!=item.end();++it)
                if(it.key()!="input" && it.key()!="output" && it.key()!="explain") error(label+" 含有未知字段 "+it.key());
            for(const auto* key:{"input","output"}) {
                std::string text;
                if(!stringAt(item,key,text) || text.empty()) error(label+"."+key+" 不能为空");
            }
            if(item.contains("explain")) {
                const auto& explain=item.at("explain");
                if(!explain.is_object()) error(label+".explain 必须是对象");
                else {
                    for(auto it=explain.begin();it!=explain.end();++it)
                        if(it.key()!="zh" && it.key()!="en") error(label+".explain 含有未知字段 "+it.key());
                    for(const auto* key:{"zh","en"})
                        if(explain.contains(key) && !explain.at(key).is_string()) error(label+".explain."+key+" 必须是字符串");
                }
            }
        }
    }
    // ---- 2：组与分值 ----
    long long pointsSum=0;
    std::set<std::string> groupNames,allCases;
    if(!document.contains("groups") || !document.at("groups").is_array()) error("groups 缺失或不是数组");
    else {
        const auto& groups=document.at("groups");
        if(groups.size()<2) error("groups 至少需要 2 组（含 sample）");
        for(std::size_t i=0;i<groups.size();++i) {
            const auto& group=groups[i];
            auto label="groups["+std::to_string(i)+"]";
            if(!group.is_object()) { error(label+" 必须是对象"); continue; }
            for(auto it=group.begin();it!=group.end();++it)
                if(it.key()!="name" && it.key()!="points" && it.key()!="cases") error(label+" 含有未知字段 "+it.key());
            std::string name;
            if(!stringAt(group,"name",name) || name.empty()) error(label+".name 不能为空");
            else {
                if(i==0) { if(name!="sample") error("第一组必须是 sample 组"); }
                else if(!validGroupName(name)) error(label+".name 格式不合法：需匹配 ^[a-z][a-z0-9_-]{0,15}$");
                if(!groupNames.insert(name).second) error("组名 "+name+" 重复");
            }
            long long points=0;
            if(!integerAt(group,"points",points)) error(label+".points 必须是整数");
            else if(points<0) error(label+".points 不能为负");
            else {
                if(i==0 && points!=1) error("样例组 points 必须为 1");
                pointsSum+=points;
            }
            if(!group.contains("cases") || !group.at("cases").is_array()) error(label+".cases 必须是数组");
            else {
                const auto& cases=group.at("cases");
                if(cases.empty()) error(label+".cases 至少需要 1 个用例");
                for(std::size_t k=0;k<cases.size();++k) {
                    if(!cases[k].is_string()) { error(label+".cases["+std::to_string(k)+"] 必须是字符串"); continue; }
                    auto caseId=cases[k].get<std::string>();
                    if(!validCaseId(caseId)) error("用例 id "+caseId+" 格式不合法");
                    if(!allCases.insert(caseId).second) error("用例 "+caseId+" 出现在多个组中");
                }
            }
        }
        if(pointsSum!=100) error("groups 分值之和为 "+std::to_string(pointsSum)+"，应为 100");
    }
    // ---- 4：function 模式 ----
    if(structure.functionMode) {
        if(!document.contains("function") || !document.at("function").is_object()) error("function 模式必须提供 function 段");
        else {
            const auto& function=document.at("function");
            for(auto it=function.begin();it!=function.end();++it)
                if(it.key()!="package" && it.key()!="signature" && it.key()!="drivers" && it.key()!="starter")
                    error("function 含有未知字段 "+it.key());
            std::string package;
            if(!stringAt(function,"package",package) || trim(package).empty()) error("function.package 不能为空");
            else if(package.find_first_of(" \t\r\n/\\")!=std::string::npos) error("function.package 含有非法字符");
            if(!function.contains("signature") || !function.at("signature").is_object()) error("function.signature 缺失或不是对象");
            else {
                const auto& signature=function.at("signature");
                for(auto it=signature.begin();it!=signature.end();++it)
                    if(it.key()!="zh" && it.key()!="en") error("function.signature 含有未知字段 "+it.key());
                for(const auto* key:{"zh","en"}) {
                    std::string text;
                    if(!stringAt(signature,key,text) || trim(text).empty()) error(std::string("function.signature.")+key+" 不能为空");
                }
            }
            for(const auto* key:{"drivers","starter"}) {
                if(!function.contains(key) || !function.at(key).is_object()) { error(std::string("function.")+key+" 缺失或不是对象"); continue; }
                for(auto it=function.at(key).begin();it!=function.at(key).end();++it) {
                    if(it.key()!="cpp" && it.key()!="cangjie") error(std::string("function.")+key+" 含有未知语言 "+it.key());
                    else if(!it.value().is_string() || trim(it.value().get<std::string>()).empty()) error(std::string("function.")+key+"."+it.key()+" 不能为空");
                }
            }
            if(function.contains("drivers") && function.at("drivers").is_object() && function.contains("starter") && function.at("starter").is_object()) {
                const auto& drivers=function.at("drivers");
                const auto& starter=function.at("starter");
                bool any=false;
                for(const auto* language:{"cpp","cangjie"}) {
                    bool hasDriver=drivers.contains(language),hasStarter=starter.contains(language);
                    if(hasDriver!=hasStarter) error(std::string("function.drivers 与 function.starter 的语言集合不一致：")+language);
                    if(hasDriver && hasStarter) { structure.drivers.push_back(language); any=true; }
                }
                if(!any) error("function.drivers 至少需要 cpp 或 cangjie 之一");
            }
        }
    }
    std::string checker;
    if(!stringAt(document,"checker",checker) || trim(checker).empty()) error("checker 不能为空");
    else if(checker.size()>512*1024) error("checker 超过 512 KB");
    else structure.checker=checker;

    if(!document.contains("solution") || !document.at("solution").is_object()) error("solution 缺失或不是对象");
    else {
        const auto& solution=document.at("solution");
        if(solution.empty()) error("solution 至少需要一种语言");
        for(auto it=solution.begin();it!=solution.end();++it) {
            auto language=it.key();
            if(language!="cpp" && language!="cangjie") { error("solution 含有未知语言 "+language); continue; }
            std::size_t size=0; bool ok=true;
            if(it.value().is_string()) size=it.value().get_ref<const std::string&>().size();
            else if(it.value().is_array()) {
                if(it.value().empty()) { error("solution."+language+" 不能是空数组"); ok=false; }
                for(std::size_t i=0;i<it.value().size() && ok;++i) {
                    const auto& unit=it.value()[i];
                    if(!unit.is_string() || unit.get_ref<const std::string&>().empty()) { error("solution."+language+"["+std::to_string(i)+"] 必须是非空字符串"); ok=false; break; }
                    size+=unit.get_ref<const std::string&>().size()+1;
                }
            } else { error("solution."+language+" 必须是字符串或字符串数组"); ok=false; }
            if(!ok) continue;
            if(size>512*1024) { error("solution."+language+" 超过 512 KB"); continue; }
            if(structure.functionMode && std::find(structure.drivers.begin(),structure.drivers.end(),language)==structure.drivers.end()) {
                error("solution 声明了 "+language+"，但题包没有对应的 driver");
                continue;
            }
            structure.solutions.push_back(language);
        }
    }
    if(document.contains("notes")) {
        if(!document.at("notes").is_object()) error("notes 必须是对象");
        else for(auto it=document.at("notes").begin();it!=document.at("notes").end();++it)
            if(it.key()!="zh" && it.key()!="en") error("notes 含有未知字段 "+it.key());
    }
    // ---- 3：用例来源 ----
    bool hasTests=document.contains("tests");
    if(hasTests) {
        const auto& tests=document.at("tests");
        if(!tests.is_array()) error("tests 必须是数组");
        else {
            if(tests.size()>200) error("用例数超过 200（"+std::to_string(tests.size())+" 个）");
            std::size_t totalBytes=0;
            for(std::size_t i=0;i<tests.size();++i) {
                const auto& item=tests[i];
                auto label="tests["+std::to_string(i)+"]";
                if(!item.is_object()) { error(label+" 必须是对象"); continue; }
                for(auto it=item.begin();it!=item.end();++it)
                    if(it.key()!="id" && it.key()!="group" && it.key()!="input" && it.key()!="answer") error(label+" 含有未知字段 "+it.key());
                ProblemCase entry;
                if(!stringAt(item,"id",entry.id) || !validCaseId(entry.id)) error(label+".id 缺失或格式不合法");
                if(!stringAt(item,"group",entry.group)) error(label+".group 缺失");
                if(!stringAt(item,"input",entry.input)) error(label+".input 缺失");
                else if(entry.input.size()>4*1024*1024) error("用例 "+entry.id+" 的输入超过 4 MiB");
                if(!stringAt(item,"answer",entry.answer) || entry.answer.empty()) error("用例 "+entry.id+" 缺少答案");
                else if(entry.answer.size()>4*1024*1024) error("用例 "+entry.id+" 的答案超过 4 MiB");
                totalBytes+=entry.input.size()+entry.answer.size();
                if(!entry.id.empty()) structure.cases.push_back(std::move(entry));
            }
            if(totalBytes>64ULL*1024*1024) error("用例总大小超过 64 MiB");
            structure.hasTests=true;
        }
    } else if(document.contains("testsZipPath")) {
        std::string zipPath;
        if(!stringAt(document,"testsZipPath",zipPath)) error("testsZipPath 必须是字符串");
        else {
            auto path=fs::path(wide(zipPath));
            if(!path.is_absolute()) error("testsZipPath 必须是绝对路径");
            else if(!fs::is_regular_file(path)) error("找不到 testsZipPath 指向的数据包："+zipPath);
            else structure.zipPath=zipPath;
        }
    }
    if(!hasTests && structure.zipPath.empty()) error("tests 与 testsZipPath 至少要提供一个");
}

// ---- 3：把用例真的取到内存里（zip 需要解压） ----
std::vector<ProblemCase> collectCases(const Json& document,const Structure& structure,const fs::path& workspace,Issues& issues) {
    auto error=[&](std::string message) { issues.error(std::move(message)); };
    std::vector<std::pair<std::string,std::string>> ordered;
    std::set<std::string> listed;
    for(const auto& group:document.at("groups"))
        for(const auto& item:group.at("cases")) {
            ordered.emplace_back(item.get<std::string>(),group.at("name").get<std::string>());
            listed.insert(item.get<std::string>());
        }
    std::vector<ProblemCase> cases;
    if(structure.hasTests) {
        std::map<std::string,const ProblemCase*> byId;
        for(const auto& entry:structure.cases) byId[entry.id]=&entry;
        for(const auto& [id,group]:ordered) {
            auto it=byId.find(id);
            if(it==byId.end()) { error("用例 "+id+" 不在 tests 中"); continue; }
            if(!it->second->group.empty() && it->second->group!=group)
                error("用例 "+id+" 在 tests 里属于组 "+it->second->group+"，但 groups 把它列在组 "+group);
            auto entry=*it->second; entry.group=group;
            cases.push_back(std::move(entry));
        }
        for(const auto& entry:structure.cases)
            if(!listed.contains(entry.id)) error("用例 "+entry.id+" 不在任何组中");
    } else {
        auto extracted=workspace/"data";
        try { extractZip(fs::path(wide(structure.zipPath)),extracted); }
        catch(const std::exception& e) { error(std::string("读取 data.zip 失败：")+e.what()); return {}; }
        std::map<std::string,fs::path> inputs,answers;
        for(const auto& entry:fs::directory_iterator(extracted)) {
            if(!entry.is_regular_file()) continue;
            auto name=utf8(entry.path().stem().wstring());
            auto extension=utf8(entry.path().extension().wstring());
            if(extension==".in") inputs[name]=entry.path();
            else if(extension==".ans") answers[name]=entry.path();
        }
        std::size_t totalBytes=0;
        for(const auto& [id,group]:ordered) {
            if(!inputs.contains(id)) { error("用例 "+id+" 缺少 "+id+".in"); continue; }
            if(!answers.contains(id)) { error("用例 "+id+" 缺少 "+id+".ans"); continue; }
            ProblemCase entry{id,group,stripBom(readFile(inputs[id])),stripBom(readFile(answers[id]))};
            if(entry.input.size()>4*1024*1024) error("用例 "+id+" 的输入超过 4 MiB");
            if(entry.answer.empty()) error("用例 "+id+" 的 .ans 是空文件");
            else if(entry.answer.size()>4*1024*1024) error("用例 "+id+" 的答案超过 4 MiB");
            totalBytes+=entry.input.size()+entry.answer.size();
            cases.push_back(std::move(entry));
        }
        for(const auto& [id,path]:inputs) { (void)path; if(!listed.contains(id)) error("用例 "+id+" 不在任何组中"); }
        for(const auto& [id,path]:answers) { (void)path; if(!listed.contains(id)) error("用例 "+id+" 不在任何组中"); }
        if(totalBytes>64ULL*1024*1024) error("用例总大小超过 64 MiB");
        if(cases.size()>200) error("用例数超过 200");
    }
    return cases;
}
Program compileReference(const Json& document,const Structure& structure,const std::string& language,const fs::path& directory,const Json& tools) {
    auto units=unitsOf(document.at("solution").at(language));
    if(structure.functionMode) {
        const auto& function=document.at("function");
        auto driver=function.at("drivers").at(language).get<std::string>();
        auto package=function.at("package").get<std::string>();
        if(language=="cpp") return buildUnit(language,{{"Main.cpp",assembleCpp(driver,units)}},directory,tools,nullptr);
        return buildUnit(language,assembleCangjie(driver,package,units,true),directory,tools,nullptr);
    }
    if(units.size()==1) return compileProgram(units[0],language,directory,tools,nullptr);
    if(language=="cpp") return buildUnit(language,{{"Main.cpp",assembleCpp("",units)}},directory,tools,nullptr);
    return buildUnit(language,assembleCangjie("","",units,false),directory,tools,nullptr);
}
// ---- 6–8：编译 checker / driver / 用参考答案跑满分 ----
Json verifyPackage(const Json& document,const Structure& structure,const std::vector<ProblemCase>& cases,const fs::path& workspace,const Json& tools,Issues& issues) {
    auto error=[&](std::string message) { issues.error(std::move(message)); };
    auto caseDirectory=workspace/"cases";
    fs::create_directories(caseDirectory);
    std::map<std::string,std::pair<fs::path,fs::path>> paths;
    for(const auto& item:cases) {
        auto input=caseDirectory/wide(item.id+".in"),answer=caseDirectory/wide(item.id+".ans");
        writeFile(input,item.input);
        writeFile(answer,item.answer);
        paths[item.id]={input,answer};
    }
    auto checkerDirectory=workspace/"checker";
    fs::create_directories(checkerDirectory);
    writeFile(checkerDirectory/L"testlib.h",testlib_asset::header);
    auto checker=buildChecker(structure.checker,checkerDirectory,tools,nullptr);
    if(checker.verdict!="AC") {
        error("checker 编译失败（前 20 行）：\n"+firstLines(checker.log,20));
        return Json::object();
    }
    Json driverStatus=Json::object();
    if(structure.functionMode) {
        for(const auto& language:structure.drivers) {
            const auto& function=document.at("function");
            auto driver=function.at("drivers").at(language).get<std::string>();
            auto starter=function.at("starter").at(language).get<std::string>();
            auto package=function.at("package").get<std::string>();
            Program program;
            if(language=="cpp") program=buildUnit(language,{{"Main.cpp",assembleCpp(driver,{starter})}},workspace/L"driver-cpp",tools,nullptr);
            else program=buildUnit(language,assembleCangjie(driver,package,{starter},true),workspace/L"driver-cangjie",tools,nullptr);
            driverStatus[language]=program.verdict=="AC";
            if(program.verdict!="AC") error("drivers."+language+" 编译失败（前 20 行）：\n"+firstLines(program.log,20));
        }
    }
    Json solutions=Json::object(),groupStatus=Json::array();
    long long timeMs=document.at("limits").value("timeMs",2000LL);
    long long memoryMb=document.at("limits").value("memoryMb",512LL);
    for(const auto& language:structure.solutions) {
        auto directory=workspace/wide("solution-"+language);
        auto program=compileReference(document,structure,language,directory,tools);
        if(program.verdict!="AC") {
            error("参考答案（"+language+"）编译失败（前 20 行）：\n"+firstLines(program.log,20));
            continue;
        }
        long long score=0; std::string firstFailure,firstGroup,firstCase,firstMessage;
        Json groupsHere=Json::array();
        for(const auto& group:document.at("groups")) {
            bool passed=true;
            auto groupName=group.at("name").get<std::string>();
            for(const auto& caseItem:group.at("cases")) {
                auto id=caseItem.get<std::string>();
                auto runDirectory=workspace/"run"/wide(language+"-"+id);
                fs::create_directories(runDirectory);
                CaseFile file{id,groupName,paths[id].first,paths[id].second,fs::file_size(paths[id].second)};
                auto judgement=judgeCase(program,runDirectory,file,checker,timeMs,memoryMb,nullptr);
                if(judgement.verdict!="AC") {
                    passed=false;
                    if(firstFailure.empty()) { firstFailure=judgement.verdict; firstGroup=groupName; firstCase=id; firstMessage=judgement.message; }
                    break;
                }
            }
            groupsHere.push_back({{"name",groupName},{"points",group.at("points")},{"passed",passed}});
            if(passed) score+=group.at("points").get<long long>();
        }
        solutions[language]={{"score",score},{"verdict",firstFailure.empty()?"AC":firstFailure}};
        if(groupStatus.empty()) groupStatus=groupsHere;
        if(score!=100) {
            if(!firstFailure.empty()) {
                auto detail=firstMessage.empty()?std::string():("："+firstMessage.substr(0,600));
                error("参考答案未满分：组 "+firstGroup+" 未通过（用例 "+firstCase+" "+firstFailure+"）"+detail);
            } else error("参考答案未满分：得分 "+std::to_string(score)+"，应为 100");
        }
    }
    return {{"cases",static_cast<long long>(cases.size())},{"groups",groupStatus},{"checkerCompiled",true},
            {"drivers",driverStatus},{"solutions",solutions}};
}
Json readRequest(const Json& request) {
    std::string text;
    if(request.contains("json") && request.at("json").is_string()) text=request.at("json").get<std::string>();
    else if(request.contains("path") && request.at("path").is_string()) {
        auto path=request.at("path").get<std::string>();
        if(path.empty()) throw ApiError(400,"path 不能为空");
        auto file=fs::path(wide(path));
        if(!file.is_absolute()) throw ApiError(400,"path 必须是绝对路径");
        if(!fs::is_regular_file(file)) throw ApiError(400,"找不到题包文件："+path);
        text=readFile(file);
    } else throw ApiError(400,"请提供 json 或 path");
    if(text.size()>64ULL*1024*1024) throw ApiError(400,"problem.json 超过 64 MiB");
    try { return Json::parse(text); }
    catch(const std::exception& e) {
        Json details=Json::array();
        details.push_back({{"level","error"},{"message",std::string("JSON 解析失败：")+e.what()}});
        throw ApiError(400,"题包校验失败",{{"details",details}});
    }
}
Json readMeta(const fs::path& directory) {
    auto path=directory/L"problem.json";
    if(!fs::is_regular_file(path)) throw ApiError(404,"题目不存在");
    try { return Json::parse(readFile(path)); }
    catch(const std::exception& e) { throw std::runtime_error("题目数据损坏："+std::string(e.what())); }
}
void summarize(const Json& meta,const std::string& id,Json& item) {
    long long total=0;
    if(meta.contains("groups") && meta.at("groups").is_array())
        for(const auto& group:meta.at("groups")) total+=group.value("points",0LL);
    item={{"id",id},{"title",meta.value("title",Json::object())},{"difficulty",meta.value("difficulty",0LL)},
          {"tags",meta.value("tags",Json::array())},{"judgeMode",meta.value("judgeMode",std::string())},
          {"limits",{{"timeMs",meta.contains("limits")?meta.at("limits").value("timeMs",0LL):0LL},
                     {"memoryMb",meta.contains("limits")?meta.at("limits").value("memoryMb",0LL):0LL}}},
          {"totalPoints",total}};
}
}

fs::path problemsRoot(const fs::path& dataDir) { return fs::absolute(dataDir).parent_path()/L"problems"; }

Json listProblems(const fs::path& dataDir) {
    auto root=problemsRoot(dataDir),cacheRoot=executableDirectory();
    Json items=Json::array();
    std::error_code error;
    if(fs::is_directory(root,error)) {
        for(const auto& entry:fs::directory_iterator(root,error)) {
            if(!entry.is_directory()) continue;
            std::string id=utf8(entry.path().filename().wstring());
            if(!validId(id)) continue;
            try {
                auto meta=readMeta(entry.path());
                Json item; summarize(meta,id,item);
                item.update(problemStats(cacheRoot,id));
                items.push_back(std::move(item));
            } catch(const std::exception& e) {
                std::fprintf(stderr,"JudgeBox: 跳过无法读取的题目 %s：%s\n",id.c_str(),e.what());
            }
        }
    }
    auto rank=[](const Json& item) { return item.at("bestScore").is_null()?-1LL:item.at("bestScore").get<long long>(); };
    std::sort(items.begin(),items.end(),[&](const Json& a,const Json& b){
        auto left=rank(a),right=rank(b);
        if(left!=right) return left<right;
        auto difficultyA=a.value("difficulty",0LL),difficultyB=b.value("difficulty",0LL);
        if(difficultyA!=difficultyB) return difficultyA<difficultyB;
        return a.value("id",std::string())<b.value("id",std::string());
    });
    return {{"problems",items}};
}

Json loadProblem(const fs::path& dataDir,const std::string& id) {
    if(!validId(id)) throw ApiError(404,"题目不存在");
    auto directory=problemsRoot(dataDir)/wide(id);
    auto meta=readMeta(directory);
    Json item; summarize(meta,id,item);
    item.update(problemStats(executableDirectory(),id));
    Json function=meta.value("function",Json::object());
    Json groups=Json::array();
    if(meta.contains("groups") && meta.at("groups").is_array())
        for(const auto& group:meta.at("groups")) {
            auto caseCount=group.contains("cases") && group.at("cases").is_array()?group.at("cases").size():0;
            groups.push_back({{"name",group.at("name")},{"points",group.at("points")},{"cases",group.at("cases")},{"caseCount",static_cast<long long>(caseCount)}});
        }
    Json languages=Json::array();
    if(meta.value("judgeMode",std::string())=="function") {
        auto drivers=function.value("drivers",Json::object());
        for(const auto* language:{"cpp","cangjie"}) if(drivers.contains(language)) languages.push_back(language);
    } else { languages.push_back("cpp"); languages.push_back("cangjie"); }
    item.update({{"statement",meta.value("statement",Json::object())},
                 {"hints",meta.value("hints",Json::object())},
                 {"samples",meta.value("samples",Json::array())},
                 {"signature",function.value("signature",Json::object())},
                 {"starter",function.value("starter",Json::object())},
                 {"drivers",function.value("drivers",Json::object())},
                 {"groups",groups},
                 {"judgedLanguages",languages}});
    return item;
}

Json importProblem(const fs::path& dataDir,const Json& request) {
    auto document=readRequest(request);
    Structure structure; Issues issues;
    validateDocument(document,structure,issues);
    if(!issues.empty()) mergeDetails(issues,"题包校验失败");
    if(request.contains("zipPath") && request.at("zipPath").is_string()) {
        auto zipPath=request.at("zipPath").get<std::string>();
        auto path=fs::path(wide(zipPath));
        if(!path.is_absolute()) issues.error("zipPath 必须是绝对路径");
        else if(!fs::is_regular_file(path)) issues.error("找不到 zipPath 指向的数据包："+zipPath);
        else { structure.zipPath=zipPath; structure.hasTests=false; structure.cases.clear(); }
        if(!issues.empty()) mergeDetails(issues,"题包校验失败");
    }
    auto root=problemsRoot(dataDir);
    fs::create_directories(root);
    Workspace workspace(root/wide(".import-"+std::to_string(GetTickCount64())));
    auto cases=collectCases(document,structure,workspace.path,issues);
    if(!issues.empty() || cases.empty()) {
        if(issues.empty()) issues.error("题包没有任何用例");
        mergeDetails(issues,"题包校验失败");
    }
    auto tools=detectTools(executableDirectory());
    auto verification=verifyPackage(document,structure,cases,workspace.path,tools,issues);
    if(!issues.empty()) mergeDetails(issues,"题包校验失败");

    auto target=root/wide(structure.id);
    bool replaced=fs::is_directory(target);
    fs::create_directories(target);
    createZip(target/L"data.zip",workspace.path/"cases");
    Json meta=structure.meta;
    meta.erase("tests");
    meta["storedAt"]=nowIso();
    Json report={{"id",structure.id},{"importedAt",nowIso()},{"verification",verification}};
    writeFile(target/L"report.json",report.dump(2));
    writeFile(target/L"problem.json",meta.dump(2));
    Json result={{"ok",true},{"id",structure.id},{"verification",verification}};
    if(replaced) result["replaced"]=true;
    return result;
}

bool deleteProblem(const fs::path& dataDir,const std::string& id) {
    if(!validId(id)) return false;
    auto directory=problemsRoot(dataDir)/wide(id);
    std::error_code error;
    if(!fs::is_directory(directory,error)) return false;
    fs::remove_all(directory,error);
    if(error) throw std::runtime_error("无法删除题目目录："+utf8(directory.wstring()));
    removeProblemSubmissions(executableDirectory(),id);
    return true;
}

ProblemPackage openProblem(const fs::path& dataDir,const std::string& id,const fs::path& workDirectory) {
    if(!validId(id)) throw ApiError(404,"题目不存在");
    ProblemPackage package;
    package.directory=problemsRoot(dataDir)/wide(id);
    package.meta=readMeta(package.directory);
    if(!package.meta.contains("groups") || !package.meta.at("groups").is_array()) throw std::runtime_error("题目数据损坏：groups 缺失");
    auto zip=package.directory/L"data.zip";
    if(!fs::is_regular_file(zip)) throw std::runtime_error("题目数据损坏：缺少 data.zip");
    fs::create_directories(workDirectory);
    extractZip(zip,workDirectory);
    for(const auto& group:package.meta.at("groups")) {
        auto groupName=group.at("name").get<std::string>();
        for(const auto& item:group.at("cases")) {
            CaseFile file;
            file.id=item.get<std::string>();
            file.group=groupName;
            file.input=workDirectory/wide(file.id+".in");
            file.answer=workDirectory/wide(file.id+".ans");
            if(!fs::is_regular_file(file.input)) throw std::runtime_error("题目数据损坏：缺少 "+file.id+".in");
            if(!fs::is_regular_file(file.answer)) throw std::runtime_error("题目数据损坏：缺少 "+file.id+".ans");
            file.answerBytes=fs::file_size(file.answer);
            package.cases.push_back(std::move(file));
        }
    }
    return package;
}
