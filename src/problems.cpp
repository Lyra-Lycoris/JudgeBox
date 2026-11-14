#include "problems.hpp"
#include "apierror.hpp"
#include "compiler.hpp"
#include "problemjudge.hpp"
#include "submitstore.hpp"
#include "ziputil.hpp"
#include "testlib_asset.hpp"
#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <mutex>
#include <map>
#include <set>
#include <string_view>

namespace {
const std::set<std::string> kFields={"schemaVersion","id","title","difficulty","tags","limits","judgeMode","statement",
    "samples","groups","function","notes"};
const std::set<std::string> kTags={"模拟","枚举","排序","二分","贪心","构造","前缀和","差分","双指针","滑动窗口","哈希","栈",
    "队列","单调栈","堆","并查集","树状数组","线段树","字符串","Trie","KMP","图论","最短路","最小生成树","拓扑排序","二分图",
    "网络流","树","最近公共祖先","动态规划","背包","区间DP","状压DP","数位DP","树形DP","数学","数论","组合数学","概率期望",
    "计算几何","位运算","分治","记忆化搜索","高精度","交互"};
struct Structure {
    std::string id,checker;
    Json meta;
    std::vector<std::string> drivers,solutions;
    bool functionMode=false;
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

    // ---- 4：function 模式（package / signature 在 json 里，driver 与 starter 来自文件） ----
    if(structure.functionMode) {
        if(!document.contains("function") || !document.at("function").is_object()) error("function 模式必须提供 function 段（package 与 signature）");
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
                for(auto it=signature.begin();it!=signature.end();++it)
                    if(it.key()!="zh" && it.key()!="en") error("function.signature 含有未知字段 "+it.key());
                for(const auto* key:{"zh","en"}) {
                    std::string text;
                    if(!stringAt(signature,key,text) || trim(text).empty()) error(std::string("function.signature.")+key+" 不能为空");
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
    auto extension=[](const std::string& language) { return language=="cpp"?std::string(".cpp"):std::string(".cj"); };

    // checker.cpp 可选：没有就按内置 token 比较判
    if(present("checker.cpp")) {
        auto text=readText(directory/L"checker.cpp");
        if(trim(text).empty()) error("checker.cpp 是空文件");
        else if(text.size()>512*1024) error("checker.cpp 超过 512 KB");
        else structure.checker=text;
    }

    Json drivers=Json::object(),starter=Json::object(),solution=Json::object();
    for(const auto& language:{"cpp","cangjie"}) {
        auto name=std::string(language),main="main"+extension(name),start="starter"+extension(name);
        bool hasMain=present(main),hasStarter=present(start);
        if(structure.functionMode) {
            if(!hasMain) {
                if(hasStarter) error("有 "+start+" 但缺少 "+main+"（starter 必须和 main 成对）");
                continue;
            }
            if(!hasStarter) { error("缺少 "+start+"（function 模式每个 driver 都要配 starter）"); continue; }
            drivers[name]=readText(directory/wide(main));
            starter[name]=readText(directory/wide(start));
            structure.drivers.push_back(name);
        } else {
            if(hasMain) error("io 模式不需要 "+main+"（选手自己写 main）");
            if(hasStarter) error("io 模式不需要 "+start);
        }
    }
    if(structure.functionMode && structure.drivers.empty()) error("function 模式至少要有一个 main.cj 或 main.cpp");

    for(const auto& language:{"cpp","cangjie"}) {
        auto name=std::string(language),ext=extension(name);
        std::vector<std::string> units;
        if(present("solution"+ext)) units.push_back(readText(directory/wide("solution"+ext)));
        else {
            std::map<int,std::string> numbered;
            for(const auto& entry:fs::directory_iterator(directory)) {
                auto file=utf8(entry.path().filename().wstring());
                std::string prefix="solution_";
                if(!file.starts_with(prefix) || !file.ends_with(ext) || file.size()<=prefix.size()+ext.size()) continue;
                auto middle=file.substr(prefix.size(),file.size()-prefix.size()-ext.size());
                if(middle.find_first_not_of("0123456789")!=std::string::npos) continue;
                numbered[std::stoi(middle)]=readText(entry.path());
            }
            for(const auto& [index,text]:numbered) {
                if(index!=static_cast<int>(units.size())+1) { error("solution_ 编号必须从 1 连续（缺 solution_"+std::to_string(units.size()+1)+ext+"）"); break; }
                units.push_back(text);
            }
        }
        if(units.empty()) continue;
        std::size_t bytes=0;
        for(const auto& unit:units) bytes+=unit.size()+1;
        if(bytes>512*1024) { error("solution"+ext+" 超过 512 KB"); continue; }
        if(structure.functionMode && std::find(structure.drivers.begin(),structure.drivers.end(),name)==structure.drivers.end()) {
            error("有 solution"+ext+"，但没有对应的 main"+ext+"（参考答案的语言必须有 driver）");
            continue;
        }
        solution[name]=units.size()==1?Json(units[0]):Json(units);
        structure.solutions.push_back(name);
    }
    if(structure.solutions.empty()) error("缺少参考解：solution.cj 或 solution.cpp（多文件用 solution_1.cj、solution_2.cj…）");

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
    structure.meta["solution"]=solution;
    if(structure.functionMode) {
        auto function=structure.meta.value("function",Json::object());
        function["drivers"]=drivers;
        function["starter"]=starter;
        structure.meta["function"]=function;
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

// ---- 6–8：编译 checker（可选）/ driver / 用参考答案跑满分 ----
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
                auto judgement=judgeCase(program,runDirectory,file,custom?&checker:nullptr,timeMs,memoryMb,nullptr);
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
    return {{"cases",static_cast<long long>(cases.size())},{"groups",groupStatus},
            {"checker",custom?"custom":"builtin"},{"checkerCompiled",custom},
            {"drivers",driverStatus},{"solutions",solutions}};
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
    item={{"id",id},{"title",meta.value("title",Json::object())},{"difficulty",meta.value("difficulty",0LL)},
          {"tags",meta.value("tags",Json::array())},{"judgeMode",meta.value("judgeMode",std::string())},
          {"limits",{{"timeMs",meta.contains("limits")?meta.at("limits").value("timeMs",0LL):0LL},
                     {"memoryMb",meta.contains("limits")?meta.at("limits").value("memoryMb",0LL):0LL}}},
          {"totalPoints",total}};
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
// 题库目录里的每个 zip 就是一道题；标题/难度等元数据全部来自包里的 problem.json。
std::vector<DatabaseFile> scanDatabase() {
    std::vector<DatabaseFile> files;
    std::error_code error;
    auto root=problemDatabase();
    if(!fs::is_directory(root,error)) return files;
    std::vector<fs::path> paths;
    for(const auto& entry:fs::directory_iterator(root,error))
        if(entry.is_regular_file() && entry.path().extension()==L".zip") paths.push_back(entry.path());
    std::sort(paths.begin(),paths.end());
    for(const auto& path:paths) {
        try {
            std::lock_guard lock(databaseMutex);
            auto key=path.wstring();
            auto stamp=stampOf(path);
            auto found=databaseCache.find(key);
            if(found!=databaseCache.end() && !stamp.empty() && found->second.stamp==stamp) {
                files.push_back({path,found->second.document});
                continue;
            }
            auto document=readZipDocument(path);
            CacheEntry entry; entry.stamp=stamp; entry.document=document;
            databaseCache[key]=entry;
            files.push_back({path,std::move(document)});
        } catch(const std::exception& e) {
            std::fprintf(stderr,"JudgeBox: 跳过无法读取的题包 %s：%s\n",utf8(path.filename().wstring()).c_str(),e.what());
        }
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
    Json languages=Json::array();
    if(meta.value("judgeMode",std::string())=="function") {
        auto drivers=function.value("drivers",Json::object());
        for(const auto* language:{"cpp","cangjie"}) if(drivers.contains(language)) languages.push_back(language);
    } else { languages.push_back("cpp"); languages.push_back("cangjie"); }
    item.update({{"statement",meta.value("statement",Json::object())},
                 {"samples",meta.value("samples",Json::array())},
                 {"signature",function.value("signature",Json::object())},
                 {"starter",function.value("starter",Json::object())},
                 {"drivers",function.value("drivers",Json::object())},
                 {"groups",groups},
                 {"judgedLanguages",languages}});
    return item;
}

Json problemMeta(const std::string& id) {
    if(!validId(id)) throw ApiError(404,"题目不存在");
    fs::path file; Json document;
    if(!findDatabaseFile(id,file,document)) throw ApiError(404,"题目不存在");
    return loadNormalized(file,document,false).meta;
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