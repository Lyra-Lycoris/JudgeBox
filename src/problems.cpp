#include "problems.hpp"
#include "apierror.hpp"
#include "compiler.hpp"
#include "problemjudge.hpp"
#include "submitstore.hpp"
#include "ziputil.hpp"
#include "testlib_asset.hpp"
#include <algorithm>
#include <atomic>
#include <cstdio>
#include <cstdlib>
#include <mutex>
#include <map>
#include <set>
#include <string_view>
#include <thread>

namespace {
const std::set<std::string> kFields={"schemaVersion","id","title","difficulty","tags","limits","judgeMode","modes","statement",
    "samples","groups","function","notes","topic","judgeType","source","selfJudge"};
// 题包 v2 的固定语言顺序（也是界面下拉框的顺序）。
const std::vector<std::string> kLanguages={"cpp","cangjie","python","java"};
bool isLanguage(const std::string& language) { return std::find(kLanguages.begin(),kLanguages.end(),language)!=kLanguages.end(); }
std::string extensionOf(const std::string& language) {
    if(language=="cpp") return ".cpp";
    if(language=="cangjie") return ".cj";
    if(language=="python") return ".py";
    if(language=="java") return ".java";
    return {};
}
std::string languageName(const std::string& language) {
    if(language=="cpp") return "C++";
    if(language=="cangjie") return "仓颉";
    if(language=="python") return "Python";
    if(language=="java") return "Java";
    return language;
}
const std::set<std::string> kTags={"模拟","枚举","排序","二分","贪心","构造","前缀和","差分","双指针","滑动窗口","哈希","栈",
    "队列","单调栈","堆","并查集","树状数组","线段树","字符串","Trie","KMP","图论","最短路","最小生成树","拓扑排序","二分图",
    "网络流","树","最近公共祖先","动态规划","背包","区间DP","状压DP","数位DP","树形DP","数学","数论","组合数学","概率期望",
    "计算几何","位运算","分治","记忆化搜索","高精度","交互"};
// 一种语言的声明：提交方式 + 函数式 driver/starter + 参考解。
// 只有函数式才需要 driver/starter；只声明完整式时 solution 就是完整程序。
struct Language {
    std::vector<std::string> modes;
    std::string driver,starter;
    std::vector<std::string> solution;
    bool function() const { return std::find(modes.begin(),modes.end(),"function")!=modes.end(); }
    bool full() const { return std::find(modes.begin(),modes.end(),"full")!=modes.end(); }
};
struct Structure {
    std::string id,checker;
    Json meta;
    int version=1;
    std::map<std::string,Language> languages;
    std::string legacyMode;   // schemaVersion 1 的 judgeMode，仅用于兼容旧题包
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
    if(!integerAt(document,"schemaVersion",version)) error("schemaVersion 缺失或不是整数");
    else if(version!=1 && version!=2) error("schemaVersion 只能是 1（旧格式）或 2（四语言 × 两提交方式）");
    else structure.version=static_cast<int>(version);

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
    // ---- 专题 / 裁判方式 / 题目来源 / 自判题：题库卡片与 solveRecord 分层用 ----
    if(document.contains("topic")) {
        std::string topic;
        if(!stringAt(document,"topic",topic) || trim(topic).empty()) error("topic 不能为空字符串");
        else if(textWidth(topic)>24) error("topic 超过 24 个字符");
    }
    if(document.contains("judgeType")) {
        std::string kind;
        if(!stringAt(document,"judgeType",kind)) error("judgeType 必须是字符串");
        else if(kind!="standard" && kind!="special" && kind!="interactive" && kind!="function")
            error("judgeType 只能是 standard（普通）、special（特殊）、interactive（交互）或 function（函数）");
    }
    if(document.contains("source")) {
        const auto& origin=document.at("source");
        if(!origin.is_object()) error("source 必须是对象");
        else {
            for(auto it=origin.begin();it!=origin.end();++it)
                if(it.key()!="platform" && it.key()!="id" && it.key()!="url") error("source 含有未知字段 "+it.key());
            std::string platform;
            if(!stringAt(origin,"platform",platform) || trim(platform).empty()) error("source.platform 不能为空");
            else if(platform!="luogu" && platform!="leetcode" && platform!="codeforces" && platform!="other")
                error("source.platform 只能是 luogu、leetcode、codeforces 或 other");
            for(const auto* key:{"id","url"}) {
                if(!origin.contains(key)) continue;
                std::string text;
                if(!stringAt(origin,key,text)) error(std::string("source.")+key+" 必须是字符串");
                else if(textWidth(text)>200) error(std::string("source.")+key+" 超过 200 个字符");
                else if(std::string(key)=="url" && !text.empty() && !text.starts_with("https://")) error("source.url 必须以 https:// 开头");
            }
        }
    }
    if(document.contains("selfJudge") && !document.at("selfJudge").is_boolean()) error("selfJudge 必须是布尔值");
    bool selfJudge=document.value("selfJudge",false);

    // ---- 提交方式：v2 用 modes（语言 → function/full），v1 仍用 judgeMode ----
    if(structure.version==2) {
        if(document.contains("judgeMode")) error("schemaVersion 2 不再使用 judgeMode，请改用 modes");
        if(selfJudge && (!document.contains("modes") || !document.at("modes").is_object())) {
            // 自判题只带测试数据：没有 driver 与参考解，默认四种语言都走完整程序提交。
            for(const auto& language:kLanguages) structure.languages[language].modes={"full"};
        } else if(!document.contains("modes") || !document.at("modes").is_object()) error("schemaVersion 2 必须提供 modes（语言 → 提交方式数组）");
        else {
            const auto& modes=document.at("modes");
            if(modes.empty()) error("modes 至少要声明一种语言");
            for(auto it=modes.begin();it!=modes.end();++it) {
                auto language=it.key();
                if(!isLanguage(language)) { error("modes 里的语言 "+language+" 不支持（只能是 cpp、cangjie、python、java）"); continue; }
                if(!it.value().is_array() || it.value().empty()) { error("modes."+language+" 必须是非空数组"); continue; }
                auto& spec=structure.languages[language];
                for(std::size_t i=0;i<it.value().size();++i) {
                    auto label="modes."+language+"["+std::to_string(i)+"]";
                    if(!it.value()[i].is_string()) { error(label+" 必须是字符串"); continue; }
                    auto mode=it.value()[i].get<std::string>();
                    if(mode!="function" && mode!="full") { error(label+" 只能是 function 或 full"); continue; }
                    if(selfJudge && mode=="function") { error(label+"：自判题（selfJudge）只有测试数据，不支持函数式提交"); continue; }
                    if(std::find(spec.modes.begin(),spec.modes.end(),mode)!=spec.modes.end()) { error("modes."+language+" 重复声明了 "+mode); continue; }
                    spec.modes.push_back(mode);
                }
            }
        }
    } else if(document.contains("modes")) {
        error("schemaVersion 1 不支持 modes，请把 schemaVersion 改成 2");
    } else {
        std::string mode;
        if(!stringAt(document,"judgeMode",mode)) error("judgeMode 缺失或不是字符串");
        else if(mode!="io" && mode!="function") error("judgeMode 只能是 io 或 function");
        else {
            structure.legacyMode=mode;
            // io：旧约定固定 C++/仓颉两种语言、完整程序提交；函数题的语言由 main.* 决定（collectPackage 填充）。
            if(mode=="io") {
                structure.languages["cpp"].modes={"full"};
                structure.languages["cangjie"].modes={"full"};
            }
        }
    }

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

    // ---- 4：函数式段（package / signature 在 json 里，driver 与 starter 来自文件） ----
    bool needsFunction=structure.legacyMode=="function";
    for(const auto& [language,spec]:structure.languages) if(spec.function()) needsFunction=true;
    if(needsFunction && (!document.contains("function") || !document.at("function").is_object()))
        error("函数式提交必须提供 function 段（package 与 signature）");
    if(document.contains("function")) {
        if(!document.at("function").is_object()) error("function 必须是对象");
        else {
            const auto& function=document.at("function");
            for(auto it=function.begin();it!=function.end();++it)
                if(it.key()!="package" && it.key()!="signature")
                    error("function 含有未知字段 "+it.key());
            std::string package;
            if(!stringAt(function,"package",package) || trim(package).empty()) error("function.package 不能为空");
            else if(package.find_first_of(" \t\r\n/\\")!=std::string::npos) error("function.package 含有非法字符");
            if(!function.contains("signature") || !function.at("signature").is_object()) error("function.signature 缺失或不是对象");
            else {
                const auto& signature=function.at("signature");
                for(auto it=signature.begin();it!=signature.end();++it) {
                    if(it.key()!="zh" && it.key()!="en" && !isLanguage(it.key()))
                        error("function.signature 含有未知字段 "+it.key());
                }
                for(const auto* key:{"zh","en"}) {
                    std::string text;
                    if(!stringAt(signature,key,text) || trim(text).empty()) error(std::string("function.signature.")+key+" 不能为空");
                }
                // 可选：按语言给出更准确的签名（cpp/cangjie/python/java），显示时优先用当前语言的那一份。
                for(const auto& language:kLanguages) {
                    if(!signature.contains(language)) continue;
                    std::string text;
                    if(!stringAt(signature,language.c_str(),text) || trim(text).empty())
                        error("function.signature."+language+" 不能为空");
                }
            }
        }
    }
    if(document.contains("notes")) {
        if(!document.at("notes").is_object()) error("notes 必须是对象");
        else for(auto it=document.at("notes").begin();it!=document.at("notes").end();++it)
            if(it.key()!="zh" && it.key()!="en") error("notes 含有未知字段 "+it.key());
    }
}


// ---- 3：从题包目录里读代码文件与用例 ----
std::vector<ProblemCase> collectPackage(const fs::path& directory,const Json& document,Structure& structure,Issues& issues,bool readCases=true) {
    auto error=[&](std::string message) { issues.error(std::move(message)); };
    for(const auto& entry:fs::directory_iterator(directory))
        if(entry.is_directory()) error("题包 zip 不能有子目录："+utf8(entry.path().filename().wstring()));
    auto readText=[&](const fs::path& path) { return stripBom(readFile(path)); };
    auto present=[&](const std::string& name) { return fs::is_regular_file(directory/wide(name)); };

    // checker.cpp 可选：没有就按内置 token 比较判
    if(present("checker.cpp")) {
        auto text=readText(directory/L"checker.cpp");
        if(trim(text).empty()) error("checker.cpp 是空文件");
        else if(text.size()>512*1024) error("checker.cpp 超过 512 KB");
        else structure.checker=text;
    }

    const bool selfJudge=document.value("selfJudge",false);
    if(structure.version==2 && selfJudge) {
        // 自判题：题包里只有测试数据，参考解 / driver / starter 一律可选（有也不校验）。
        for(const auto& language:kLanguages) {
            auto found=structure.languages.find(language);
            if(found==structure.languages.end()) continue;
            auto modeExt=extensionOf(language);
            if(present("solution"+modeExt)) found->second.solution={readText(directory/wide("solution"+modeExt))};
        }
    } else if(structure.version==2) {
        for(const auto& language:kLanguages) {
            auto found=structure.languages.find(language);
            if(found==structure.languages.end()) continue;
            auto& spec=found->second;
            auto name=languageName(language),modeExt=extensionOf(language);
            auto main="main"+modeExt,start="starter"+modeExt,solution="solution"+modeExt;
            bool hasMain=present(main),hasStarter=present(start),hasSolution=present(solution);
            if(spec.function()) {
                if(!hasMain) error("缺少 "+main+"（"+name+" 函数式 driver）");
                if(!hasStarter) error("缺少 "+start+"（"+name+" 函数式 starter）");
                if(!hasSolution) error("缺少 "+solution+"（"+name+" 函数式参考解）");
                if(hasMain) spec.driver=readText(directory/wide(main));
                if(hasStarter) spec.starter=readText(directory/wide(start));
                if(hasSolution) spec.solution={readText(directory/wide(solution))};
            } else {
                if(hasMain) error("modes 没有声明 "+name+" 的函数式提交，但题包里有 "+main);
                if(hasStarter) error("modes 没有声明 "+name+" 的函数式提交，但题包里有 "+start);
                // 只声明完整式：solution.<ext> 是完整程序（自带入口），不需要 driver/starter。
                if(!hasSolution) error("缺少 "+solution+"（"+name+" 只声明完整式提交时必须提供完整参考程序）");
                else spec.solution={readText(directory/wide(solution))};
            }
            std::size_t bytes=0;
            for(const auto& unit:spec.solution) bytes+=unit.size()+1;
            if(bytes>512*1024) error(solution+" 超过 512 KB");
        }
        // v2 一种语言只能有一个 solution.<ext>；编号多文件是 v1 的旧约定。
        for(const auto& entry:fs::directory_iterator(directory)) {
            auto file=utf8(entry.path().filename().wstring());
            if(!file.starts_with("solution_")) continue;
            fs::path path=wide(file);
            auto ext=utf8(path.extension().wstring()),stem=utf8(path.stem().wstring());
            if(ext!=".cpp" && ext!=".cj" && ext!=".py" && ext!=".java") continue;
            auto middle=stem.substr(std::string("solution_").size());
            if(!middle.empty() && middle.find_first_not_of("0123456789")==std::string::npos)
                error("schemaVersion 2 每种语言只能有一个 solution"+ext+"（不支持 solution_1 多文件）");
        }
    } else if(structure.legacyMode=="function") {
        // v1 函数式：main.<ext> + starter.<ext> 决定语言，solution 是函数实现（可多文件）。
        for(const auto& language:{"cpp","cangjie"}) {
            auto name=std::string(language),modeExt=extensionOf(name),main="main"+modeExt,start="starter"+modeExt;
            bool hasMain=present(main),hasStarter=present(start);
            if(!hasMain) { if(hasStarter) error("有 "+start+" 但缺少 "+main+"（starter 必须和 main 成对）"); continue; }
            if(!hasStarter) { error("缺少 "+start+"（函数式提交每个 driver 都要配 starter）"); continue; }
            auto& spec=structure.languages[name];
            spec.modes={"function"};
            spec.driver=readText(directory/wide(main));
            spec.starter=readText(directory/wide(start));
        }
        if(structure.languages.empty()) error("函数式提交至少要有一个 main.cj 或 main.cpp");
    } else {
        // v1 完整式：不要 main/starter；solution.<ext> 是完整程序（可多文件）。
        for(const auto& language:{"cpp","cangjie"}) {
            auto name=std::string(language),modeExt=extensionOf(name),main="main"+modeExt,start="starter"+modeExt;
            if(present(main)) error("完整式（io）不需要 "+main+"（选手自己写 main）");
            if(present(start)) error("完整式（io）不需要 "+start);
        }
    }
    // v1 的参考解（多文件编号 solution_1.*…）：函数式是函数实现，完整式是完整程序。
    if(structure.version==1) {
        for(const auto& language:{"cpp","cangjie"}) {
            auto name=std::string(language),modeExt=extensionOf(name);
            std::vector<std::string> units;
            if(present("solution"+modeExt)) units.push_back(readText(directory/wide("solution"+modeExt)));
            else {
                std::map<int,std::string> numbered;
                for(const auto& entry:fs::directory_iterator(directory)) {
                    auto file=utf8(entry.path().filename().wstring());
                    std::string prefix="solution_";
                    if(!file.starts_with(prefix) || !file.ends_with(modeExt) || file.size()<=prefix.size()+modeExt.size()) continue;
                    auto middle=file.substr(prefix.size(),file.size()-prefix.size()-modeExt.size());
                    if(middle.find_first_not_of("0123456789")!=std::string::npos) continue;
                    numbered[std::stoi(middle)]=readText(entry.path());
                }
                for(const auto& [index,text]:numbered) {
                    if(index!=static_cast<int>(units.size())+1) { error("solution_ 编号必须从 1 连续（缺 solution_"+std::to_string(units.size()+1)+modeExt+"）"); break; }
                    units.push_back(text);
                }
            }
            if(units.empty()) continue;
            std::size_t bytes=0;
            for(const auto& unit:units) bytes+=unit.size()+1;
            if(bytes>512*1024) { error("solution"+modeExt+" 超过 512 KB"); continue; }
            auto found=structure.languages.find(name);
            if(found==structure.languages.end()) {
                error("有 solution"+modeExt+"，但没有对应的 main"+modeExt+"（参考答案的语言必须有 driver）");
                continue;
            }
            found->second.solution=units;
        }
    }
    bool anySolution=false;
    for(const auto& [language,spec]:structure.languages) if(!spec.solution.empty()) anySolution=true;
    if(!anySolution && !selfJudge) error("缺少参考解：每个声明的语言都要有 solution.<ext>（旧题包可用 solution_1.cj、solution_2.cj…）");

    // 用例：根目录下的 <caseId>.in / <caseId>.ans
    std::map<std::string,fs::path> inputs,answers;
    for(const auto& entry:fs::directory_iterator(directory)) {
        if(!entry.is_regular_file()) continue;
        auto name=utf8(entry.path().stem().wstring());
        auto ext=utf8(entry.path().extension().wstring());
        if(ext==".in") inputs[name]=entry.path();
        else if(ext==".ans") answers[name]=entry.path();
    }
    std::vector<std::pair<std::string,std::string>> ordered;
    std::set<std::string> listed;
    for(const auto& group:document.at("groups"))
        for(const auto& item:group.at("cases")) {
            ordered.emplace_back(item.get<std::string>(),group.at("name").get<std::string>());
            listed.insert(item.get<std::string>());
        }
    std::vector<ProblemCase> cases;
    if(readCases) {
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
    if(cases.empty()) error("题包没有任何用例");
    }

    structure.meta=document;
    structure.meta["checker"]=structure.checker;
    Json function=structure.meta.value("function",Json::object());
    if(!function.is_object()) function=Json::object();
    Json drivers=Json::object(),starter=Json::object(),modes=Json::object(),languages=Json::array();
    for(const auto& language:kLanguages) {
        auto found=structure.languages.find(language);
        if(found==structure.languages.end()) continue;
        const auto& spec=found->second;
        languages.push_back(language);
        modes[language]=Json(spec.modes);
        if(spec.function() && !spec.driver.empty()) { drivers[language]=spec.driver; starter[language]=spec.starter; }
    }
    function["drivers"]=drivers;
    function["starter"]=starter;
    structure.meta["function"]=function;
    structure.meta["modes"]=modes;
    structure.meta["judgedLanguages"]=languages;
    // 裁判方式：没显式写就按题包内容推断（checker → 特殊；有函数式 → 函数；否则普通）。
    if(!structure.meta.contains("judgeType")) {
        std::string kind="standard";
        if(!structure.checker.empty()) kind="special";
        else {
            for(const auto& [language,spec]:structure.languages) if(spec.function()) kind="function";
        }
        structure.meta["judgeType"]=kind;
    }
    return cases;
}
Program compileReference(const Structure& structure,const std::string& language,const std::string& mode,
                         const fs::path& directory,const Json& tools) {
    const auto& spec=structure.languages.at(language);
    const auto& units=spec.solution;
    if(units.empty()) { Program program; program.verdict="JE"; program.message="没有参考解"; return program; }
    auto function=structure.meta.value("function",Json::object());
    auto package=function.value("package",std::string());
    // 函数式参考解 = driver + 函数实现；完整式参考程序 = 同一份 driver + 实现拼成的完整程序。
    if(mode=="function" || spec.function()) {
        if(language=="cpp") return buildUnit(language,{{"Main.cpp",assembleCpp(spec.driver,units)}},directory,tools,nullptr);
        if(language=="cangjie") return buildUnit(language,assembleCangjie(spec.driver,package,units,true),directory,tools,nullptr);
        return compileProgram(assembleFullSource(language,spec.driver,units[0],package),language,directory,tools,nullptr);
    }
    if(units.size()==1) return compileProgram(units[0],language,directory,tools,nullptr);
    if(language=="cpp") return buildUnit(language,{{"Main.cpp",assembleCpp("",units)}},directory,tools,nullptr);
    return buildUnit(language,assembleCangjie("",package,units,false),directory,tools,nullptr);
}

// ---- 6–8：编译 checker（可选）/ driver / 用参考答案跑满分 ----
Json verifyPackage(const Json& document,const Structure& structure,const std::vector<ProblemCase>& cases,const fs::path& workspace,const Json& tools,Issues& issues) {
    auto error=[&](std::string message) { issues.error(std::move(message)); };
    // 自判题只有测试数据，没有参考解可跑：跳过自检（判题仍按 .ans 比较）。
    if(document.value("selfJudge",false))
        return {{"cases",static_cast<long long>(cases.size())},{"groups",Json::array()},{"checker","builtin"},
                {"checkerCompiled",false},{"drivers",Json::object()},{"solutions",Json::object()},{"full",Json::object()},
                {"selfJudge",true}};
    auto caseDirectory=workspace/"cases";
    fs::create_directories(caseDirectory);
    std::map<std::string,std::pair<fs::path,fs::path>> paths;
    for(const auto& item:cases) {
        auto input=caseDirectory/wide(item.id+".in"),answer=caseDirectory/wide(item.id+".ans");
        writeFile(input,item.input);
        writeFile(answer,item.answer);
        paths[item.id]={input,answer};
    }
    Program checker;
    bool custom=!structure.checker.empty();
    if(custom) {
        auto checkerDirectory=workspace/"checker";
        fs::create_directories(checkerDirectory);
        writeFile(checkerDirectory/L"testlib.h",testlib_asset::header);
        checker=buildChecker(structure.checker,checkerDirectory,tools,nullptr);
        if(checker.verdict!="AC") {
            error("checker 编译失败（前 20 行）：\n"+firstLines(checker.log,20));
            return Json::object();
        }
    }
    Json driverStatus=Json::object(),solutions=Json::object(),fullStatus=Json::object(),groupStatus=Json::array();
    long long timeMs=document.at("limits").value("timeMs",2000LL);
    long long memoryMb=document.at("limits").value("memoryMb",512LL);
    auto function=document.value("function",Json::object());
    auto package=function.value("package",std::string());
    struct RunResult {
        long long score=0;
        std::string verdict="AC",firstGroup,firstCase,message;
        Json groups=Json::array();
    };
    auto runAll=[&](const Program& program,const std::string& label) {
        RunResult result;
        for(const auto& group:document.at("groups")) {
            bool passed=true;
            auto groupName=group.at("name").get<std::string>();
            for(const auto& caseItem:group.at("cases")) {
                auto id=caseItem.get<std::string>();
                auto runDirectory=workspace/wide("run-"+label+"-"+id);
                fs::create_directories(runDirectory);
                CaseFile file{id,groupName,paths[id].first,paths[id].second,fs::file_size(paths[id].second)};
                auto judgement=judgeCase(program,runDirectory,file,custom?&checker:nullptr,timeMs,memoryMb,nullptr);
                if(judgement.verdict!="AC") {
                    passed=false;
                    if(result.verdict=="AC") { result.verdict=judgement.verdict; result.firstGroup=groupName; result.firstCase=id; result.message=judgement.message; }
                    break;
                }
            }
            result.groups.push_back({{"name",groupName},{"points",group.at("points")},{"passed",passed}});
            if(passed) result.score+=group.at("points").get<long long>();
        }
        return result;
    };
    auto reportScore=[&](const std::string& language,const RunResult& result,bool full) {
        if(result.score==100) return;
        auto prefix=std::string(full?"完整式参考答案未满分（":"参考答案未满分（")+languageName(language)+"）";
        if(result.verdict!="AC") {
            auto detail=result.message.empty()?std::string():("："+result.message.substr(0,600));
            error(prefix+"：组 "+result.firstGroup+" 未通过（用例 "+result.firstCase+" "+result.verdict+"）"+detail);
        } else error(prefix+"：得分 "+std::to_string(result.score)+"，应为 100");
    };
    for(const auto& language:kLanguages) {
        auto found=structure.languages.find(language);
        if(found==structure.languages.end()) continue;
        const auto& spec=found->second;
        if(spec.solution.empty()) continue;   // v1 完整式题可能没有该语言的参考解
        if(spec.function()) {
            auto program=buildUnit(language,assembleFunction(language,spec.driver,spec.starter,package),
                                   workspace/wide("driver-"+language),tools,nullptr);
            driverStatus[language]=program.verdict=="AC";
            if(program.verdict!="AC") error("drivers."+language+" 编译失败（前 20 行）：\n"+firstLines(program.log,20));
            auto reference=compileReference(structure,language,"function",workspace/wide("solution-"+language),tools);
            if(reference.verdict!="AC") {
                error("参考答案（"+languageName(language)+"）编译失败（前 20 行）：\n"+firstLines(reference.log,20));
            } else {
                auto result=runAll(reference,"function-"+language);
                solutions[language]={{"score",result.score},{"verdict",result.verdict}};
                if(groupStatus.empty()) groupStatus=result.groups;
                reportScore(language,result,false);
            }
        }
        if(spec.full()) {
            // C++ / Python / Java 的函数式参考程序就是完整程序（同一个源文件），成绩直接沿用；
            // 仓颉函数式是 main.cj + solve.cj 两个文件，完整式要合并成一个文件后单独跑。
            bool reuse=spec.function() && language!="cangjie" && solutions.contains(language);
            if(reuse) {
                bool perfect=solutions.at(language).value("score",0LL)==100;
                fullStatus[language]=perfect;
                if(!perfect) error("完整式参考答案未满分（"+languageName(language)+"）");
            } else {
                auto reference=compileReference(structure,language,"full",workspace/wide("full-"+language),tools);
                if(reference.verdict!="AC") {
                    error("完整式参考答案（"+languageName(language)+"）编译失败（前 20 行）：\n"+firstLines(reference.log,20));
                    continue;
                }
                auto result=runAll(reference,"full-"+language);
                fullStatus[language]=result.score==100;
                if(!spec.function()) {
                    solutions[language]={{"score",result.score},{"verdict",result.verdict}};
                    if(groupStatus.empty()) groupStatus=result.groups;
                }
                reportScore(language,result,true);
            }
        }
    }
    return {{"cases",static_cast<long long>(cases.size())},{"groups",groupStatus},
            {"checker",custom?"custom":"builtin"},{"checkerCompiled",custom},
            {"drivers",driverStatus},{"solutions",solutions},{"full",fullStatus}};
}

bool decodeBase64(const std::string& text,std::string& bytes) {
    static const std::string alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    int buffer=0,bits=0;
    for(char c:text) {
        if(c=='=') break;
        if(c=='\r' || c=='\n' || c==' ' || c=='\t') continue;
        auto index=alphabet.find(c);
        if(index==std::string::npos) return false;
        buffer=(buffer<<6)|static_cast<int>(index);
        bits+=6;
        if(bits>=8) { bits-=8; bytes.push_back(static_cast<char>((buffer>>bits)&0xFF)); }
    }
    return true;
}
// 题包是一个 zip：解压到工作目录，返回题包根目录（允许 zip 里套一层目录）。
fs::path preparePackage(const Json& request,const fs::path& workspace,Issues& issues) {
    auto error=[&](std::string message) { issues.error(std::move(message)); };
    fs::create_directories(workspace);
    auto local=workspace/"package.zip";
    if(request.contains("zipPath") && request.at("zipPath").is_string()) {
        auto text=request.at("zipPath").get<std::string>();
        auto path=fs::path(wide(text));
        if(!path.is_absolute()) { error("zipPath 必须是绝对路径"); return {}; }
        if(!fs::is_regular_file(path)) { error("找不到题包 zip："+text); return {}; }
        // 系统 tar.exe 用的是 ANSI 参数：源路径带中文会变成 ???，先复制到工作目录的 ASCII 路径再解压。
        std::error_code copyError;
        fs::copy_file(path,local,fs::copy_options::overwrite_existing,copyError);
        if(copyError) { error("无法复制题包 zip 到临时目录："+copyError.message()); return {}; }
    } else if(request.contains("zip") && request.at("zip").is_string()) {
        std::string bytes;
        if(!decodeBase64(request.at("zip").get<std::string>(),bytes)) { error("zip 字段不是合法的 base64"); return {}; }
        if(bytes.size()>44ULL*1024*1024) { error("题包 zip 超过 44 MiB（base64 上传上限）"); return {}; }
        writeFile(local,bytes);
    } else { error("请提供题包 zip：{\"zipPath\": 绝对路径} 或 {\"zip\": base64}"); return {}; }
    auto extracted=workspace/"package";
    try { extractZip(local,extracted); }
    catch(const std::exception& e) {
        error(std::string("题包 zip 解压失败（文件名请全部用 ASCII）：")+e.what());
        return {};
    }
    if(fs::is_regular_file(extracted/L"problem.json")) return extracted;
    fs::path found;
    int count=0;
    for(const auto& entry:fs::directory_iterator(extracted))
        if(entry.is_directory() && fs::is_regular_file(entry.path()/L"problem.json")) { found=entry.path(); ++count; }
    if(count==1) return found;
    error("题包 zip 根目录没有 problem.json（不要多套目录）");
    return {};
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
    // 题单卡片直接读 zip 里的 problem.json，没有经过 collectPackage；
    // 语言顺序就按 modes 的键推出来（v1 旧题包没有 modes，卡片不展示语言）。
    Json modes=meta.value("modes",Json::object());
    Json languages=Json::array();
    for(const auto& language:kLanguages) if(modes.contains(language)) languages.push_back(language);
    std::string judgeType=meta.value("judgeType",std::string());
    if(judgeType.empty()) {
        judgeType="standard";
        for(auto it=modes.begin();it!=modes.end();++it)
            if(it.value().is_array())
                for(const auto& mode:it.value())
                    if(mode.is_string() && mode.get<std::string>()=="function") judgeType="function";
    }
    item={{"id",id},{"title",meta.value("title",Json::object())},{"difficulty",meta.value("difficulty",0LL)},
          {"tags",meta.value("tags",Json::array())},
          {"modes",modes},
          {"judgedLanguages",languages},
          {"limits",{{"timeMs",meta.contains("limits")?meta.at("limits").value("timeMs",0LL):0LL},
                     {"memoryMb",meta.contains("limits")?meta.at("limits").value("memoryMb",0LL):0LL}}},
          {"totalPoints",total},
          {"topic",meta.value("topic",std::string())},
          {"judgeType",judgeType},
          {"source",meta.value("source",Json::object())},
          {"selfJudge",meta.value("selfJudge",false)}};
}
}

fs::path problemDatabase() {
    if(const char* value=std::getenv("JUDGEBOX_PROBLEM_DATABASE"); value && *value) {
        try { return fs::path(wide(std::string(value))); } catch(...) {}
    }
    return executableDirectory()/L"ProblemDatabase";
}
fs::path problemsRoot(const fs::path& dataDir) { (void)dataDir; return problemDatabase(); }

namespace {
std::string stampOf(const fs::path& file) {
    std::error_code error;
    auto size=fs::file_size(file,error);
    if(error) return {};
    auto time=fs::last_write_time(file,error);
    if(error) return {};
    return std::to_string(size)+"@"+std::to_string(static_cast<long long>(time.time_since_epoch().count()));
}
std::string hexOf(const std::string& text) {
    std::uint64_t hash=1469598103934665603ULL;
    for(unsigned char c:text) { hash^=c; hash*=1099511628211ULL; }
    char buffer[17];
    std::snprintf(buffer,sizeof buffer,"%016llx",static_cast<unsigned long long>(hash));
    return buffer;
}
Json readZipDocument(const fs::path& file) {
    auto text=readZipEntry(file,"problem.json");
    try { return Json::parse(stripBom(text)); }
    catch(const std::exception& e) { throw std::runtime_error("problem.json 解析失败："+std::string(e.what())); }
}
struct DatabaseFile { fs::path path; Json document; };
struct CacheEntry { std::string stamp; Json document; };
std::mutex databaseMutex;
std::map<std::wstring,CacheEntry> databaseCache;
bool databaseIndexLoaded=false;
// 跨进程的元数据索引：把每个 zip 的 problem.json 与其 stamp 一起存成
// .cache/problemdb/index-<题库路径哈希>.json，下次启动只读这一个文件，不再逐个 spawn tar.exe。
// 文件名带题库路径哈希，切换题库（JUDGEBOX_PROBLEM_DATABASE / 不同 exe 目录）互不干扰。
fs::path databaseIndexFile() {
    return executableDirectory()/L".cache"/L"problemdb"/wide("index-"+hexOf(utf8(problemDatabase().wstring()))+".json");
}
void loadDatabaseIndex() {
    databaseIndexLoaded=true;
    auto path=databaseIndexFile();
    std::error_code error;
    if(!fs::is_regular_file(path,error)) return;
    try {
        auto document=Json::parse(readFile(path));
        if(document.value("version",0)!=1) return;
        auto entries=document.value("entries",Json::object());
        if(!entries.is_object()) return;
        for(auto it=entries.begin();it!=entries.end();++it) {
            auto stamp=it.value().value("stamp",std::string());
            auto problem=it.value().value("document",Json::object());
            if(stamp.empty() || !problem.is_object()) continue;
            databaseCache[wide(it.key())]={stamp,problem};
        }
    } catch(...) {
        databaseCache.clear();   // 索引坏了就当没有，重新读一遍题包
    }
}
void saveDatabaseIndex(const std::vector<fs::path>& paths) {
    Json entries=Json::object();
    {
        std::lock_guard lock(databaseMutex);
        for(const auto& path:paths) {
            auto found=databaseCache.find(path.filename().wstring());
            if(found==databaseCache.end()) continue;
            entries[utf8(path.filename().wstring())]={{"stamp",found->second.stamp},{"document",found->second.document}};
        }
        databaseCache.clear();   // 只保留当前题库目录里还有的题包，索引不会越滚越大
        for(auto it=entries.begin();it!=entries.end();++it)
            databaseCache[wide(it.key())]={it.value().value("stamp",std::string()),it.value().at("document")};
    }
    auto path=databaseIndexFile();
    std::error_code error;
    fs::create_directories(path.parent_path(),error);
    auto temporary=path;
    temporary+=L".tmp";
    try {
        Json index={{"version",1},{"entries",entries}};
        writeFile(temporary,index.dump(-1,' ',false,Json::error_handler_t::replace));
        fs::rename(temporary,path,error);
        if(error) { error.clear(); fs::remove(path,error); fs::rename(temporary,path,error); }
    } catch(...) { std::error_code cleanup; fs::remove(temporary,cleanup); }
}
// 题库目录里的每个 zip 就是一道题；标题/难度等元数据全部来自包里的 problem.json。
// 命中索引/内存缓存的题只做一次 stat；没命中的用多线程并行读（每个 zip 一次 tar.exe）。
std::vector<DatabaseFile> scanDatabase() {
    std::vector<DatabaseFile> files;
    std::error_code error;
    auto root=problemDatabase();
    if(!fs::is_directory(root,error)) return files;
    std::vector<fs::path> paths;
    for(const auto& entry:fs::directory_iterator(root,error))
        if(entry.is_regular_file() && entry.path().extension()==L".zip") paths.push_back(entry.path());
    std::sort(paths.begin(),paths.end());
    {
        std::lock_guard lock(databaseMutex);
        if(!databaseIndexLoaded) loadDatabaseIndex();
    }
    std::vector<CacheEntry> resolved(paths.size());
    std::vector<std::size_t> misses;
    for(std::size_t index=0;index<paths.size();++index) {
        auto stamp=stampOf(paths[index]);
        std::lock_guard lock(databaseMutex);
        auto found=databaseCache.find(paths[index].filename().wstring());
        if(!stamp.empty() && found!=databaseCache.end() && found->second.stamp==stamp) resolved[index]=found->second;
        else misses.push_back(index);
    }
    if(!misses.empty()) {
        // 冷启动（或新增/改过题包）：并行解出 problem.json，避免 200 多次串行 spawn。
        std::atomic<std::size_t> cursor{0};
        std::mutex errorMutex;
        auto workers=static_cast<std::size_t>(std::max(1u,std::min(8u,std::thread::hardware_concurrency())));
        workers=std::min(workers,misses.size());
        auto work=[&]() {
            for(;;) {
                auto slot=cursor.fetch_add(1);
                if(slot>=misses.size()) return;
                auto index=misses[slot];
                try {
                    auto document=readZipDocument(paths[index]);
                    resolved[index]={stampOf(paths[index]),std::move(document)};
                } catch(const std::exception& e) {
                    std::lock_guard lock(errorMutex);
                    std::fprintf(stderr,"JudgeBox: 跳过无法读取的题包 %s：%s\n",
                                 utf8(paths[index].filename().wstring()).c_str(),e.what());
                }
            }
        };
        std::vector<std::thread> pool;
        for(std::size_t i=1;i<workers;++i) pool.emplace_back(work);
        work();
        for(auto& thread:pool) thread.join();
        for(auto index:misses) {
            if(resolved[index].stamp.empty()) continue;
            std::lock_guard lock(databaseMutex);
            databaseCache[paths[index].filename().wstring()]=resolved[index];
        }
        saveDatabaseIndex(paths);
    }
    for(std::size_t index=0;index<paths.size();++index) {
        if(resolved[index].stamp.empty()) continue;
        files.push_back({paths[index],std::move(resolved[index].document)});
    }
    return files;
}
// 解压到 .cache/problemdb/<stamp>，同一份题包只解一次；判题与详情都从这里读。
fs::path extractedRoot(const fs::path& file) {
    auto directory=executableDirectory()/L".cache"/L"problemdb"/wide(hexOf(utf8(file.filename().wstring())+"\n"+stampOf(file)));
    auto package=directory/L"package";
    if(fs::is_regular_file(package/L"problem.json")) return package;
    std::error_code error;
    fs::remove_all(directory,error);
    fs::create_directories(directory);
    auto alias=directory/L"source.zip";
    fs::create_hard_link(file,alias,error);
    if(error) { error.clear(); fs::copy_file(file,alias,fs::copy_options::overwrite_existing,error); }
    if(error) throw std::runtime_error("无法准备题包解压："+error.message());
    try { extractZip(alias,package); }
    catch(...) { std::error_code cleanup; fs::remove(alias,cleanup); throw; }
    fs::remove(alias,error);
    if(fs::is_regular_file(package/L"problem.json")) return package;
    fs::path found; int count=0;
    for(const auto& entry:fs::directory_iterator(package))
        if(entry.is_directory() && fs::is_regular_file(entry.path()/L"problem.json")) { found=entry.path(); ++count; }
    if(count!=1) throw std::runtime_error("题包根目录没有 problem.json（不要多套目录）");
    return found;
}
struct LoadedProblem { fs::path root; Json meta; };
LoadedProblem loadNormalized(const fs::path& file,const Json& document,bool readCases) {
    Structure structure; Issues issues;
    validateDocument(document,structure,issues);
    if(!issues.empty()) throw std::runtime_error(issues.details.front().value("message",std::string("题包不合法")));
    auto root=extractedRoot(file);
    collectPackage(root,document,structure,issues,readCases);
    if(!issues.empty()) throw std::runtime_error(issues.details.front().value("message",std::string("题包不合法")));
    structure.meta["storedAt"]=stampOf(file);
    return {root,structure.meta};
}
bool findDatabaseFile(const std::string& id,fs::path& file,Json& document) {
    for(const auto& item:scanDatabase())
        if(item.document.value("id",std::string())==id) { file=item.path; document=item.document; return true; }
    return false;
}
std::string databaseTitle(const Json& document) {
    std::string title;
    if(document.contains("title") && document.at("title").is_object()) {
        title=document.at("title").value("zh",std::string());
        if(trim(title).empty()) title=document.at("title").value("en",std::string());
    }
    if(trim(title).empty()) title="problem";
    for(char& c:title)
        if(std::string("\\/:*?\"<>|").find(c)!=std::string::npos || static_cast<unsigned char>(c)<0x20) c='-';
    while(!title.empty() && (title.back()==' ' || title.back()=='.' || title.back()=='-')) title.pop_back();
    std::size_t count=0,cut=title.size();
    for(std::size_t i=0;i<title.size();++i)
        if((static_cast<unsigned char>(title[i])&0xC0)!=0x80 && ++count==41) { cut=i; break; }
    title.resize(cut);
    if(title.empty()) title="problem";
    return title;
}
void removeExtracted(const fs::path& file) {
    std::error_code error;
    fs::remove_all(executableDirectory()/L".cache"/L"problemdb"/wide(hexOf(utf8(file.filename().wstring())+"\n"+stampOf(file))),error);
}
}

Json listProblems(const fs::path& dataDir) {
    (void)dataDir;
    auto cacheRoot=executableDirectory();
    Json items=Json::array();
    for(const auto& item:scanDatabase()) {
        auto id=item.document.value("id",std::string());
        if(!validId(id)) continue;
        Json card; summarize(item.document,id,card);
        auto title=card.value("title",Json::object());
        auto text=[&](const char* key) {
            return title.is_object() && title.contains(key) && title.at(key).is_string()
                ? title.at(key).get<std::string>() : std::string();
        };
        if(trim(text("zh")).empty() || trim(text("en")).empty()) {
            auto fallback=utf8(item.path.stem().wstring());
            Json fixed=title.is_object()?title:Json::object();
            if(trim(text("zh")).empty()) fixed["zh"]=fallback;
            if(trim(text("en")).empty()) fixed["en"]=fallback;
            card["title"]=fixed;
        }
        card["file"]=utf8(item.path.filename().wstring());
        card.update(problemStats(cacheRoot,id));
        items.push_back(std::move(card));
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
    (void)dataDir;
    if(!validId(id)) throw ApiError(404,"题目不存在");
    fs::path file; Json document;
    if(!findDatabaseFile(id,file,document)) throw ApiError(404,"题目不存在");
    auto meta=loadNormalized(file,document,false).meta;
    Json item; summarize(meta,id,item);
    item.update(problemStats(executableDirectory(),id));
    Json function=meta.value("function",Json::object());
    Json groups=Json::array();
    if(meta.contains("groups") && meta.at("groups").is_array())
        for(const auto& group:meta.at("groups")) {
            auto caseCount=group.contains("cases") && group.at("cases").is_array()?group.at("cases").size():0;
            groups.push_back({{"name",group.at("name")},{"points",group.at("points")},{"cases",group.at("cases")},{"caseCount",static_cast<long long>(caseCount)}});
        }
    item.update({{"statement",meta.value("statement",Json::object())},
                 {"samples",meta.value("samples",Json::array())},
                 {"signature",function.value("signature",Json::object())},
                 {"starter",function.value("starter",Json::object())},
                 {"drivers",function.value("drivers",Json::object())},
                 {"package",function.value("package",std::string())},
                 {"groups",groups},
                 {"modes",meta.value("modes",Json::object())},
                 {"judgedLanguages",meta.value("judgedLanguages",Json::array())}});
    return item;
}

Json problemMeta(const std::string& id) {
    if(!validId(id)) throw ApiError(404,"题目不存在");
    fs::path file; Json document;
    if(!findDatabaseFile(id,file,document)) throw ApiError(404,"题目不存在");
    return loadNormalized(file,document,false).meta;
}

namespace {
const std::set<std::string> kPackageFiles={"checker.cpp","main.cpp","starter.cpp","solution.cpp","main.cj","starter.cj",
    "solution.cj","main.py","starter.py","solution.py","main.java","starter.java","solution.java"};
// 把请求里的 cases 写成 <id>.in / <id>.ans，并给出分组（没给 groups 就自动均分）。
Json writeCases(const fs::path& directory,const Json& cases,const Json& requestedGroups,Issues& issues) {
    if(!cases.is_array()) { issues.error("cases 必须是数组"); return Json::array(); }
    std::error_code ignored;
    for(const auto& entry:fs::directory_iterator(directory,ignored)) {
        if(!entry.is_regular_file()) continue;
        auto ext=utf8(entry.path().extension().wstring());
        if(ext==".in" || ext==".ans") fs::remove(entry.path(),ignored);
    }
    std::vector<std::string> ids;
    std::size_t index=0;
    for(const auto& item:cases) {
        auto label="cases["+std::to_string(index)+"]";
        if(!item.is_object()) { issues.error(label+" 必须是对象"); ++index; continue; }
        std::string id;
        if(item.contains("id") && item.at("id").is_string()) id=item.at("id").get<std::string>();
        else { char buffer[16]; std::snprintf(buffer,sizeof buffer,"%02zu",index+1); id=buffer; }
        if(!validCaseId(id)) { issues.error("用例 id "+id+" 格式不合法"); ++index; continue; }
        auto input=item.value("input",std::string());
        auto answer=item.value("answer",item.value("output",std::string()));
        if(trim(answer).empty()) { issues.error("用例 "+id+" 的预期输出为空（.ans 不能是空文件）"); ++index; continue; }
        if(input.size()>4*1024*1024) { issues.error("用例 "+id+" 的输入超过 4 MiB"); ++index; continue; }
        if(answer.size()>4*1024*1024) { issues.error("用例 "+id+" 的预期输出超过 4 MiB"); ++index; continue; }
        if(!input.empty() && input.back()!='\n') input+='\n';
        if(answer.back()!='\n') answer+='\n';
        writeFile(directory/wide(id+".in"),input);
        writeFile(directory/wide(id+".ans"),answer);
        ids.push_back(id);
        ++index;
    }
    if(ids.empty()) { issues.error("至少需要一个测试用例"); return Json::array(); }
    if(requestedGroups.is_array() && !requestedGroups.empty()) return requestedGroups;
    Json groups=Json::array();
    if(ids.size()==1) {
        Json single=Json::array(); single.push_back(ids[0]);
        groups.push_back({{"name","sample"},{"points",100},{"cases",single}});
        return groups;
    }
    Json sampleCases=Json::array(); sampleCases.push_back(ids[0]);
    groups.push_back({{"name","sample"},{"points",1},{"cases",sampleCases}});
    std::vector<std::string> rest(ids.begin()+1,ids.end());
    const int parts=rest.size()>=3?3:static_cast<int>(rest.size());
    const char* names[3]={"easy","medium","hard"};
    int remainingPoints=99;
    std::size_t cursor=0;
    for(int part=0;part<parts;++part) {
        auto count=rest.size()/parts+(static_cast<std::size_t>(part)<rest.size()%parts?1:0);
        Json list=Json::array();
        for(std::size_t i=0;i<count && cursor<rest.size();++i) list.push_back(rest[cursor++]);
        int points=part==parts-1?remainingPoints:remainingPoints/(parts-part);
        remainingPoints-=points;
        groups.push_back({{"name",parts==1?"main":names[part]},{"points",points},{"cases",list}});
    }
    return groups;
}
void listPackageFiles(const fs::path& directory,Json& files) {
    files=Json::object();
    std::error_code error;
    for(const auto& entry:fs::directory_iterator(directory,error)) {
        if(!entry.is_regular_file()) continue;
        auto name=utf8(entry.path().filename().wstring());
        if(!kPackageFiles.contains(name)) continue;
        if(entry.file_size()>600*1024) continue;
        files[name]=stripBom(readFile(entry.path()));
    }
}
Json packageCases(const fs::path& directory,const Json& document) {
    Json cases=Json::array();
    std::size_t total=0;
    if(!document.contains("groups") || !document.at("groups").is_array()) return cases;
    for(const auto& group:document.at("groups")) {
        if(!group.contains("cases") || !group.at("cases").is_array()) continue;
        for(const auto& item:group.at("cases")) {
            auto id=item.get<std::string>();
            auto inputPath=directory/wide(id+".in"),answerPath=directory/wide(id+".ans");
            if(!fs::is_regular_file(inputPath) || !fs::is_regular_file(answerPath)) continue;
            auto inputSize=fs::file_size(inputPath),answerSize=fs::file_size(answerPath);
            if(total+inputSize+answerSize>8ULL*1024*1024) continue;
            total+=inputSize+answerSize;
            cases.push_back({{"id",id},{"group",group.value("name",std::string())},
                             {"input",stripBom(readFile(inputPath))},{"answer",stripBom(readFile(answerPath))}});
        }
    }
    return cases;
}
}
Json saveProblem(const fs::path& dataDir,const Json& request) {
    auto id=request.value("id",std::string());
    if(!validId(id)) throw ApiError(400,"id 格式不合法：需匹配 ^[a-z0-9][a-z0-9-]{1,47}$");
    const bool edit=request.value("edit",false);
    Workspace workspace(executableDirectory()/L".cache"/L"save"/wide(std::to_string(GetTickCount64())+"-"+std::to_string(GetCurrentThreadId())));
    auto package=workspace.path/"package";
    fs::create_directories(package);
    Json document=Json::object();
    if(edit) {
        fs::path file; Json existing;
        if(!findDatabaseFile(id,file,existing)) throw ApiError(404,"题目不存在");
        // 题库里的 zip 名带中文，而 tar.exe 的 argv 走 ANSI：先复制到工作目录的 ASCII 路径再解压。
        auto alias=workspace.path/"source.zip";
        std::error_code copyError;
        fs::copy_file(file,alias,fs::copy_options::overwrite_existing,copyError);
        if(copyError) throw ApiError(500,"无法读取旧题包："+copyError.message());
        extractZip(alias,package);
        if(!fs::is_regular_file(package/L"problem.json")) {
            fs::path found; int count=0;
            for(const auto& entry:fs::directory_iterator(package))
                if(entry.is_directory() && fs::is_regular_file(entry.path()/L"problem.json")) { found=entry.path(); ++count; }
            if(count==1) package=found;
        }
        if(!fs::is_regular_file(package/L"problem.json")) throw ApiError(500,"旧题包解压后找不到 problem.json");
        document=Json::parse(stripBom(readFile(package/L"problem.json")));
    } else {
        document={{"schemaVersion",2},{"id",id}};
    }
    // 元数据按字段覆盖：title/limits/statement/function 允许只传一部分（深度合并），其余整体替换。
    for(const auto* key:{"title","difficulty","tags","limits","statement","samples","modes","function","notes","topic","judgeType","source","selfJudge"}) {
        if(!request.contains(key)) continue;
        auto mergeable=std::string(key)=="title" || std::string(key)=="limits" || std::string(key)=="statement" || std::string(key)=="function";
        if(mergeable && document.contains(key) && document[key].is_object() && request.at(key).is_object()) document[key].update(request.at(key));
        else document[key]=request.at(key);
    }
    document["schemaVersion"]=2;
    document["id"]=id;
    if(!document.contains("topic")) document["topic"]=request.value("topic",std::string("未分类"));

    Issues issues;
    if(request.contains("files")) {
        if(!request.at("files").is_object()) issues.error("files 必须是对象（文件名 → 内容）");
        else for(auto it=request.at("files").begin();it!=request.at("files").end();++it) {
            auto name=it.key();
            if(!kPackageFiles.contains(name)) { issues.error("files 里不支持的文件名 "+name); continue; }
            if(!it.value().is_string()) { issues.error("files."+name+" 必须是字符串"); continue; }
            writeFile(package/wide(name),it.value().get<std::string>());
        }
        if(!issues.empty()) mergeDetails(issues,"题目保存失败");
    }
    if(request.contains("cases")) {
        auto groups=writeCases(package,request.at("cases"),request.value("groups",Json::array()),issues);
        if(!issues.empty()) mergeDetails(issues,"题目保存失败");
        document["groups"]=groups;
    } else if(!edit) throw ApiError(400,"新建题目需要提供 cases（测试数据）");
    // 没有声明 modes 又没有参考解：按“只带测试数据、由自己程序自判”的题处理。
    bool hasSolution=false;
    if(!document.contains("modes")) {
        hasSolution=fs::is_regular_file(package/L"solution.cpp") || fs::is_regular_file(package/L"solution.cj") ||
                    fs::is_regular_file(package/L"solution.py") || fs::is_regular_file(package/L"solution.java");
        document["selfJudge"]=!hasSolution;
        Json defaults=Json::object();
        for(const auto& language:kLanguages) defaults[language]=Json::array({"full"});
        document["modes"]=defaults;
    }
    if(document.value("selfJudge",false)) {
        // 自判题没有 driver：把所有语言的提交方式收敛到完整程序。
        Json modes=Json::object();
        for(const auto& language:kLanguages) modes[language]=Json::array({"full"});
        document["modes"]=modes;
    }
    writeFile(package/L"problem.json",document.dump(2)+"\n");
    auto archive=workspace.path/"package.zip";
    createZip(archive,package);
    Json result=importProblem(dataDir,{{"zipPath",utf8(archive.wstring())}});
    result["edit"]=edit;
    result["selfJudge"]=document.value("selfJudge",false);
    return result;
}

Json packageDetail(const fs::path& dataDir,const std::string& id) {
    (void)dataDir;
    if(!validId(id)) throw ApiError(404,"题目不存在");
    fs::path file; Json document;
    if(!findDatabaseFile(id,file,document)) throw ApiError(404,"题目不存在");
    auto root=extractedRoot(file);
    Json files; listPackageFiles(root,files);
    return {{"id",id},{"file",utf8(file.filename().wstring())},{"meta",document},{"files",files},
            {"cases",packageCases(root,document)}};
}

Json problemCases(const fs::path& dataDir,const std::string& id) {
    (void)dataDir;
    if(!validId(id)) throw ApiError(404,"题目不存在");
    fs::path file; Json document;
    if(!findDatabaseFile(id,file,document)) throw ApiError(404,"题目不存在");
    auto root=extractedRoot(file);
    auto cases=packageCases(root,document);
    return {{"id",id},{"cases",cases},{"count",static_cast<long long>(cases.size())}};
}

// 题库编辑器用：从本地目录里收集成对的 .in / .ans，直接当成新题的测试数据。
Json scanCaseDirectory(const std::string& directory) {
    auto text=trim(directory);
    if(text.empty()) throw ApiError(400,"请填写数据目录的绝对路径");
    auto root=fs::path(wide(text));
    std::error_code error;
    if(!fs::is_directory(root,error)) throw ApiError(404,"目录不存在："+text);
    std::map<std::string,fs::path> inputs,answers;
    for(const auto& entry:fs::directory_iterator(root,error)) {
        if(!entry.is_regular_file()) continue;
        auto name=utf8(entry.path().stem().wstring());
        auto ext=utf8(entry.path().extension().wstring());
        if(ext==".in") inputs[name]=entry.path();
        else if(ext==".ans") answers[name]=entry.path();
    }
    std::vector<std::string> ids;
    for(const auto& [id,path]:inputs) { (void)path; if(answers.contains(id)) ids.push_back(id); }
    std::sort(ids.begin(),ids.end());
    Json cases=Json::array();
    std::size_t total=0;
    for(const auto& id:ids) {
        if(cases.size()>=200) break;
        auto inputSize=fs::file_size(inputs[id],error);
        auto answerSize=fs::file_size(answers[id],error);
        if(error || total+inputSize+answerSize>16ULL*1024*1024) continue;
        if(inputSize>4ULL*1024*1024 || answerSize>4ULL*1024*1024) continue;
        total+=inputSize+answerSize;
        cases.push_back({{"id",id},{"input",stripBom(readFile(inputs[id]))},{"answer",stripBom(readFile(answers[id]))}});
    }
    if(cases.empty()) throw ApiError(400,"目录里没有成对的 .in / .ans 文件");
    return {{"directory",text},{"cases",cases},{"count",static_cast<long long>(cases.size())}};
}

Json importProblem(const fs::path& dataDir,const Json& request) {
    (void)dataDir;
    Workspace workspace(executableDirectory()/L".cache"/L"import"/wide(std::to_string(GetTickCount64())));
    Issues issues;
    auto package=preparePackage(request,workspace.path,issues);
    if(!issues.empty()) mergeDetails(issues,"题包校验失败");
    Json document;
    try { document=Json::parse(stripBom(readFile(package/L"problem.json"))); }
    catch(const std::exception& e) {
        issues.error(std::string("problem.json 解析失败：")+e.what());
        mergeDetails(issues,"题包校验失败");
    }
    Structure structure;
    validateDocument(document,structure,issues);
    if(!issues.empty()) mergeDetails(issues,"题包校验失败");
    auto cases=collectPackage(package,document,structure,issues,true);
    if(!issues.empty()) mergeDetails(issues,"题包校验失败");
    auto tools=detectTools(executableDirectory());
    auto verification=verifyPackage(structure.meta,structure,cases,workspace.path,tools,issues);
    if(!issues.empty()) mergeDetails(issues,"题包校验失败");

    auto database=problemDatabase();
    fs::create_directories(database);
    bool replaced=false;
    std::error_code error;
    for(const auto& item:scanDatabase())
        if(item.document.value("id",std::string())==structure.id) {
            removeExtracted(item.path);
            fs::remove(item.path,error);
            replaced=true;
        }
    auto name=structure.id+"_"+databaseTitle(document)+"_.zip";
    auto target=database/wide(name);
    std::error_code copyError;
    fs::copy_file(workspace.path/"package.zip",target,fs::copy_options::overwrite_existing,copyError);
    if(copyError) throw std::runtime_error("无法写入题库目录："+copyError.message());
    Json result={{"ok",true},{"id",structure.id},{"file",name},{"verification",verification}};
    if(replaced) result["replaced"]=true;
    return result;
}

bool deleteProblem(const fs::path& dataDir,const std::string& id) {
    (void)dataDir;
    if(!validId(id)) return false;
    bool removed=false;
    std::error_code error;
    for(const auto& item:scanDatabase())
        if(item.document.value("id",std::string())==id) {
            removeExtracted(item.path);
            fs::remove(item.path,error);
            removed=true;
        }
    if(removed) removeProblemSubmissions(executableDirectory(),id);
    return removed;
}

ProblemPackage openProblem(const fs::path& dataDir,const std::string& id,const fs::path& workDirectory) {
    (void)dataDir; (void)workDirectory;
    if(!validId(id)) throw ApiError(404,"题目不存在");
    fs::path file; Json document;
    if(!findDatabaseFile(id,file,document)) throw ApiError(404,"题目不存在");
    auto loaded=loadNormalized(file,document,false);
    ProblemPackage package;
    package.directory=loaded.root;
    package.meta=loaded.meta;
    if(!package.meta.contains("groups") || !package.meta.at("groups").is_array()) throw std::runtime_error("题目数据损坏：groups 缺失");
    for(const auto& group:package.meta.at("groups")) {
        auto groupName=group.at("name").get<std::string>();
        for(const auto& item:group.at("cases")) {
            CaseFile entry;
            entry.id=item.get<std::string>();
            entry.group=groupName;
            entry.input=loaded.root/wide(entry.id+".in");
            entry.answer=loaded.root/wide(entry.id+".ans");
            if(!fs::is_regular_file(entry.input)) throw std::runtime_error("题目数据损坏：缺少 "+entry.id+".in");
            if(!fs::is_regular_file(entry.answer)) throw std::runtime_error("题目数据损坏：缺少 "+entry.id+".ans");
            entry.answerBytes=fs::file_size(entry.answer);
            package.cases.push_back(std::move(entry));
        }
    }
    return package;
}