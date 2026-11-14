#include "problemjudge.hpp"
#include "apierror.hpp"
#include "checker.hpp"
#include "path_compat.hpp"
#include "submitstore.hpp"
#include "testlib_asset.hpp"
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <map>
#include <string_view>

namespace {
struct JudgeFailure {
    std::string verdict,message;
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
// 规格 §7.3：选手文件首行不是 package 时要补上题包声明的包名。
std::string ensurePackage(const std::string& source,const std::string& package) {
    auto text=stripBom(source);
    auto start=text.find_first_not_of(" \t\r\n");
    if(start!=std::string::npos) {
        std::string_view rest(text);
        rest.remove_prefix(start);
        if(rest.starts_with("package") && rest.size()>7 && (rest[7]==' ' || rest[7]=='\t')) return text;
    }
    return "package "+package+"\n\n"+text;
}
std::string firstLines(const std::string& log,std::size_t maxLines) {
    std::string result; std::size_t start=0,lines=0;
    while(start<log.size() && lines<maxLines) {
        auto end=log.find('\n',start);
        if(end==std::string::npos) end=log.size();
        result+=log.substr(start,end-start); result+='\n'; ++lines; start=end+1;
    }
    if(result.size()>8000) result.resize(8000);
    return result;
}
std::string nowIso() {
    SYSTEMTIME now; GetSystemTime(&now);
    char buffer[64];
    std::snprintf(buffer,sizeof(buffer),"%04d-%02d-%02dT%02d:%02d:%02dZ",now.wYear,now.wMonth,now.wDay,now.wHour,now.wMinute,now.wSecond);
    return buffer;
}
fs::path compilerPath(const std::string& tool) {
    auto path=fs::path(wide(tool));
    wchar_t shortName[32768]; DWORD length=GetShortPathNameW(path.c_str(),shortName,32768);
    if(length && length<32768) path=shortName;
    if(path.empty()) return path;
    auto parent=path.parent_path();
    if(parent.filename()==L"bin") path=asciiDirectory(parent.parent_path())/L"bin"/path.filename();
    else path=asciiDirectory(parent)/path.filename();
    return path;
}
void classifyCompile(Program& program,const runResult& result) {
    program.log=result.stdOut+result.errOut;
    if(result.cancelled) { program.verdict="CANCELLED"; program.message="已停止编译"; }
    else if(!result.started || !result.errorMessage.empty()) { program.verdict="JE"; program.message="编译器启动失败："+result.errorMessage; }
    else if(result.TLE || result.MLE || result.OLE) { program.verdict="JE"; program.message="编译器超过资源限制（60 秒 / 2 GiB / 2 MiB 输出）"; }
    else if(result.exit>=0xC0000000UL) { program.verdict="JE"; program.message="编译器异常退出（Windows 状态 "+std::to_string(result.exit)+"），请检查工具链依赖"; }
    else if(result.exit) { program.verdict="CE"; program.message="编译失败，请查看编译日志"; }
}
}

std::string assembleCpp(const std::string& driver,const std::vector<std::string>& units) {
    std::string source;
    if(!driver.empty()) { source=driver; source+='\n'; }
    for(const auto& unit:units) { source+=unit; source+='\n'; }
    return source;
}
std::vector<std::pair<std::string,std::string>> assembleCangjie(const std::string& driver,const std::string& package,
                                                                 const std::vector<std::string>& units,bool functionMode) {
    std::vector<std::pair<std::string,std::string>> files;
    if(functionMode) files.emplace_back("main.cj",driver);
    for(std::size_t i=0;i<units.size();++i) {
        auto name=i==0?(functionMode?"solve.cj":"main.cj"):"solve_"+std::to_string(i+1)+".cj";
        // cjc 要求同一编译单元里每个 .cj 都声明相同的 package：缺省会落到 default 包，
        // 直接报 "more than one package declaration"。所以补齐包名，而不是剥掉后面文件的 package 行。
        files.emplace_back(name,functionMode?ensurePackage(units[i],package):stripBom(units[i]));
    }
    return files;
}
Program buildChecker(const std::string& source,const fs::path& directory,const Json& tools,const std::atomic_bool* cancel) {
    Program program;
    auto compiler=tools.value("cpp",std::string());
    if(compiler.empty() || !fs::is_regular_file(fs::path(wide(compiler)))) {
        program.verdict="JE"; program.message="找不到 C++ 编译器（g++），无法编译 checker";
        return program;
    }
    fs::create_directories(directory);
    writeFile(directory/L"checker.cpp",source);
    auto path=compilerPath(compiler);
    for(const auto* key:{L"GCC_EXEC_PREFIX",L"COMPILER_PATH",L"LIBRARY_PATH",L"CPATH",L"CPLUS_INCLUDE_PATH",L"C_INCLUDE_PATH"})
        program.environment.emplace_back(key,L"");
    program.pathEntries.push_back(path.parent_path().wstring());
    // testlib 版 checker 用 -O2 编译要 6~7 s，而它只取决于 checker 源码、testlib.h 和编译器本身，
    // 所以按这三者的哈希缓存到 <exe 目录>/.cache/checkers/，导入自检与每次提交都复用同一份。
    std::uint64_t hash=1469598103934665603ULL;
    auto mix=[&hash](std::string_view text){ for(unsigned char c:text) { hash^=c; hash*=1099511628211ULL; } hash^=0xff; hash*=1099511628211ULL; };
    mix(source); mix(testlib_asset::header); mix(utf8(path.wstring())); mix("c++20 -O2 v1");
    char key[17]; std::snprintf(key,sizeof key,"%016llx",static_cast<unsigned long long>(hash));
    auto cached=executableDirectory()/L".cache"/L"checkers"/wide(key)/L"checker.exe";
    if(fs::is_regular_file(cached)) { program.exe=cached.wstring(); return program; }
    RunOptions options;
    options.timeMs=60000;
    options.memoryBytes=2ULL*1024*1024*1024;
    options.outputBytes=2*1024*1024;
    options.workingDirectory=directory.wstring();
    options.cancel=cancel;
    options.pathEntries=program.pathEntries;
    options.environment=program.environment;
    auto result=runProcess(path.wstring(),{L"-std=c++20",L"-O2",L"-pipe",L"-fdiagnostics-color=never",
        L"-finput-charset=UTF-8",L"-I.",L"checker.cpp",L"-o",L"checker.exe"},"",options);
    classifyCompile(program,result);
    if(program.verdict!="AC") return program;
    program.exe=(directory/L"checker.exe").wstring();
    if(!fs::is_regular_file(directory/L"checker.exe")) { program.verdict="JE"; program.message="g++ 没有产出 checker.exe"; return program; }
    // 先写临时名再改名：导入（服务线程）与判题（工作线程）可能同时编译同一个 checker。
    std::error_code ec;
    fs::create_directories(cached.parent_path(),ec);
    auto temporary=cached.parent_path()/(L"checker-"+std::to_wstring(GetCurrentThreadId())+L".tmp");
    if(!ec && fs::copy_file(directory/L"checker.exe",temporary,fs::copy_options::overwrite_existing,ec)) {
        fs::rename(temporary,cached,ec);
        if(ec) fs::remove(temporary,ec);
    }
    return program;
}
Program buildUnit(const std::string& language,const std::vector<std::pair<std::string,std::string>>& files,
                  const fs::path& directory,const Json& tools,const std::atomic_bool* cancel) {
    Program program;
    if(files.empty()) { program.verdict="JE"; program.message="没有可编译的源码"; return program; }
    auto compiler=tools.value(language=="cpp"?"cpp":"cangjie",std::string());
    if(compiler.empty() || !fs::is_regular_file(fs::path(wide(compiler)))) {
        program.verdict="JE";
        program.message=std::string("找不到")+(language=="cpp"?"C++ 编译器（g++）":"仓颉编译器（cjc）")+"，请在工具链设置里配置";
        return program;
    }
    fs::create_directories(directory);
    auto path=compilerPath(compiler);
    auto bin=path.parent_path();
    std::vector<std::wstring> args;
    if(language=="cpp") {
        for(const auto* key:{L"GCC_EXEC_PREFIX",L"COMPILER_PATH",L"LIBRARY_PATH",L"CPATH",L"CPLUS_INCLUDE_PATH",L"C_INCLUDE_PATH"})
            program.environment.emplace_back(key,L"");
        args={L"-std=c++20",L"-O2",L"-pipe",L"-fdiagnostics-color=never",L"-finput-charset=UTF-8"};
        for(const auto& [name,content]:files) { writeFile(directory/wide(name),content); args.push_back(wide(name)); }
        args.insert(args.end(),{L"-o",L"Main.exe"});
    } else {
        auto home=bin.parent_path();
        program.environment.emplace_back(L"CANGJIE_HOME",home.wstring());
        for(const auto& part:{L"runtime/lib/windows_x86_64_cjnative",L"lib/windows_x86_64_cjnative",L"tools/bin",L"tools/lib"})
            program.pathEntries.push_back((home/part).wstring());
        for(const auto& [name,content]:files) { writeFile(directory/wide(name),content); args.push_back(wide(name)); }
        args.insert(args.end(),{L"-o",L"Main.exe",L"--diagnostic-format",L"noColor"});
    }
    program.pathEntries.push_back(bin.wstring());
    RunOptions options;
    options.timeMs=60000;
    options.memoryBytes=2ULL*1024*1024*1024;
    options.outputBytes=2*1024*1024;
    options.workingDirectory=(language=="cangjie"?asciiDirectory(directory):directory).wstring();
    options.cancel=cancel;
    options.pathEntries=program.pathEntries;
    options.environment=program.environment;
    auto result=runProcess(path.wstring(),args,"",options);
    classifyCompile(program,result);
    if(program.verdict!="AC") return program;
    program.exe=(directory/L"Main.exe").wstring();
    if(!fs::is_regular_file(directory/L"Main.exe")) { program.verdict="JE"; program.message="编译器没有产出 Main.exe"; }
    return program;
}
CaseJudgement judgeCase(const Program& program,const fs::path& directory,const CaseFile& test,const Program* checker,
                        long long timeMs,long long memoryMb,const std::atomic_bool* cancel) {
    CaseJudgement judgement;
    auto stdoutPath=directory/L"out.txt";
    RunOptions options;
    options.timeMs=timeMs;
    options.memoryBytes=static_cast<std::uint64_t>(memoryMb)*1024*1024;
    options.outputBytes=std::max<std::size_t>(1024*1024,static_cast<std::size_t>(test.answerBytes)+1024*1024);
    options.workingDirectory=directory.wstring();
    options.inputPath=test.input.wstring();
    options.stdoutPath=stdoutPath.wstring();
    options.cancel=cancel;
    options.pathEntries=program.pathEntries;
    options.environment=program.environment;
    auto run=runProcess(program.exe,program.args,"",options);
    judgement.timeMs=run.runTimeMs;
    judgement.memoryBytes=run.runMemory;
    if(run.cancelled) { judgement.verdict="CANCELLED"; judgement.message="已停止"; return judgement; }
    if(!run.started || !run.errorMessage.empty()) { judgement.verdict="JE"; judgement.message="运行失败："+run.errorMessage; return judgement; }
    if(run.MLE) { judgement.verdict="MLE"; judgement.message="触发 Windows 作业提交内存硬上限"; return judgement; }
    if(run.OLE) { judgement.verdict="OLE"; judgement.message="stdout 和 stderr 总量超过输出限制"; return judgement; }
    if(run.TLE) { judgement.verdict="TLE"; judgement.message="超过时间限制 "+std::to_string(timeMs)+" ms"; return judgement; }
    if(run.exit) { judgement.verdict="RE"; judgement.message="程序退出码："+std::to_string(run.exit); return judgement; }
    if(!checker) {
        // 题包没有 checker.cpp：按 token 比较（忽略行尾空白与空行差异）
        auto comparison=compareOutputFiles(stdoutPath,test.answer,"tokens",1e-6);
        if(comparison.equal) { judgement.verdict="AC"; return judgement; }
        judgement.verdict="WA";
        judgement.message=trim(comparison.message);
        if(judgement.message.size()>4096) judgement.message.resize(4096);
        if(judgement.message.empty()) judgement.message="输出与答案不一致";
        return judgement;
    }
    RunOptions checkOptions;
    checkOptions.timeMs=10000;
    checkOptions.memoryBytes=512ULL*1024*1024;
    checkOptions.outputBytes=32*1024;
    checkOptions.workingDirectory=directory.wstring();
    checkOptions.cancel=cancel;
    // checker 由内置 g++ 编译出来，运行时同样需要它自己的 bin 目录（libstdc++ 等 DLL）。
    checkOptions.pathEntries=checker->pathEntries;
    checkOptions.environment=checker->environment;
    auto check=runProcess(checker->exe,{test.input.wstring(),stdoutPath.wstring(),test.answer.wstring()},"",checkOptions);
    if(check.cancelled) { judgement.verdict="CANCELLED"; judgement.message="已停止"; return judgement; }
    if(!check.started || !check.errorMessage.empty() || check.TLE || check.MLE || check.OLE) {
        judgement.verdict="JE";
        judgement.message="checker 运行失败："+(check.errorMessage.empty()?"超过限制或异常退出":check.errorMessage);
        return judgement;
    }
    if(check.exit==0) { judgement.verdict="AC"; return judgement; }
    judgement.verdict="WA";
    judgement.message=trim(check.stdOut+check.errOut);
    if(judgement.message.size()>4096) judgement.message.resize(4096);
    if(judgement.message.empty()) {
        std::error_code error;
        auto bytes=fs::is_regular_file(stdoutPath,error)?fs::file_size(stdoutPath,error):0ULL;
        judgement.message="输出与答案不一致（checker 退出码 "+std::to_string(check.exit)+"，out.txt "+std::to_string(bytes)+" 字节，答案 "+std::to_string(test.answerBytes)+" 字节）";
    }
    return judgement;
}

ProblemJudgeEngine::ProblemJudgeEngine(fs::path cache,fs::path data,Json toolchain)
    : cacheRoot(std::move(cache)),dataDir(std::move(data)),tools(std::move(toolchain)) {
    state={{"submissionId",""},{"done",true},{"phase","就绪"},{"completed",0},{"total",0},{"verdict","READY"},
           {"score",0},{"best",Json(nullptr)},{"previousBest",Json(nullptr)},{"improved",false},{"finishedAt",""},
           {"groups",Json::array()},{"cases",Json::array()},{"message",""},{"compileLog",""}};
}
ProblemJudgeEngine::~ProblemJudgeEngine() {
    stop();
    if(worker.joinable()) worker.join();
}
void ProblemJudgeEngine::update(const Json& fields) {
    std::lock_guard lock(mutex);
    state.update(fields);
}
Json ProblemJudgeEngine::status() {
    std::lock_guard lock(mutex);
    return state;
}
void ProblemJudgeEngine::stop() { cancel=true; }
Json ProblemJudgeEngine::start(const Json& request) {
    {
        std::lock_guard lock(mutex);
        if(!state.at("done").get<bool>()) throw ApiError(409,"已有提交正在判题");
    }
    auto problemId=request.value("problemId",std::string());
    auto language=request.value("language",std::string());
    auto source=request.value("source",std::string());
    if(problemId.empty()) throw ApiError(400,"缺少 problemId");
    if(language!="cpp" && language!="cangjie") throw ApiError(400,"language 只能是 cpp 或 cangjie");
    if(source.empty()) throw ApiError(400,"源码不能为空");
    if(source.size()>1024*1024) throw ApiError(400,"源码不能超过 1 MiB");
    auto problem=loadProblem(dataDir,problemId);
    bool supported=false;
    for(const auto& item:problem.at("judgedLanguages")) if(item.get<std::string>()==language) supported=true;
    if(!supported) throw ApiError(400,"该题不支持所选语言");
    long long total=0;
    Json groups=Json::array();
    for(const auto& group:problem.at("groups")) {
        total+=group.value("caseCount",0LL);
        groups.push_back({{"name",group.at("name")},{"points",group.at("points")},{"earned",0},{"state","pending"}});
    }
    auto previous=bestFor(cacheRoot,problemId);
    Json best=previous.is_null()?Json(nullptr):previous.at("score");
    if(worker.joinable()) worker.join();
    auto submissionId=newSubmissionId();
    auto directory=cacheRoot/L".cache"/L"judge"/wide(submissionId);
    fs::create_directories(directory);
    cancel=false;
    {
        std::lock_guard lock(mutex);
        state={{"submissionId",submissionId},{"done",false},{"phase","准备题包"},{"completed",0},{"total",total},
               {"verdict","RUNNING"},{"score",0},{"best",best},{"previousBest",best},{"improved",false},
               {"finishedAt",""},{"groups",groups},{"cases",Json::array()},{"message",""},{"compileLog",""}};
    }
    worker=std::thread(&ProblemJudgeEngine::execute,this,request,directory);
    return {{"ok",true},{"submissionId",submissionId}};
}
void ProblemJudgeEngine::execute(Json request,fs::path directory) {
    auto problemId=request.value("problemId",std::string());
    auto language=request.value("language",std::string());
    auto source=request.value("source",std::string());
    auto snapshot=status();
    auto submissionId=snapshot.value("submissionId",std::string());
    auto total=snapshot.value("total",0LL);
    auto previousBest=snapshot.at("previousBest");
    auto groups=snapshot.at("groups");
    auto startedAt=nowIso();
    auto started=std::chrono::steady_clock::now();
    std::string verdict="AC",message,compileLog;
    Json cases=Json::array();
    long long score=0,completed=0;
    try {
        auto package=openProblem(dataDir,problemId,directory/"data");
        std::map<std::string,const CaseFile*> index;
        for(const auto& item:package.cases) index[item.id]=&item;
        update({{"phase",package.meta.value("checker",std::string()).empty()?"准备判题":"编译 checker"}});
        Program checker;
        bool customChecker=!package.meta.value("checker",std::string()).empty();
        if(customChecker) {
            auto checkerDirectory=directory/"checker";
            fs::create_directories(checkerDirectory);
            writeFile(checkerDirectory/L"testlib.h",testlib_asset::header);
            checker=buildChecker(package.meta.value("checker",std::string()),checkerDirectory,tools,&cancel);
            if(checker.verdict=="CANCELLED") throw JudgeFailure{"CANCELLED","已停止任务"};
            if(checker.verdict!="AC") throw JudgeFailure{"JE","checker 编译失败（前 20 行）：\n"+firstLines(checker.log,20)};
        }
        update({{"phase","编译提交"}});
        auto buildDirectory=directory/"build";
        auto function=package.meta.value("function",Json::object());
        Program program;
        if(package.meta.value("judgeMode",std::string())=="function") {
            auto driver=function.at("drivers").at(language).get<std::string>();
            auto packageName=function.at("package").get<std::string>();
            if(language=="cpp") program=buildUnit(language,{{"Main.cpp",assembleCpp(driver,{source})}},buildDirectory,tools,&cancel);
            else program=buildUnit(language,assembleCangjie(driver,packageName,{source},true),buildDirectory,tools,&cancel);
        } else program=compileProgram(source,language,buildDirectory,tools,&cancel);
        compileLog=program.log;
        if(compileLog.size()>64*1024) { compileLog.resize(64*1024); compileLog+="\n…（编译日志已截断）"; }
        update({{"compileLog",compileLog}});
        if(program.verdict!="AC") throw JudgeFailure{program.verdict,program.message};
        auto limits=package.meta.value("limits",Json::object());
        long long timeMs=limits.value("timeMs",2000LL),memoryMb=limits.value("memoryMb",512LL);
        int groupIndex=-1;
        for(const auto& group:package.meta.at("groups")) {
            ++groupIndex;
            auto groupName=group.at("name").get<std::string>();
            long long points=group.value("points",0LL);
            groups[groupIndex]["state"]="running";
            update({{"groups",groups}});
            bool passed=true;
            for(const auto& caseItem:group.at("cases")) {
                auto id=caseItem.get<std::string>();
                if(cancel.load()) throw JudgeFailure{"CANCELLED","已停止任务"};
                update({{"phase","运行测试点 "+std::to_string(completed+1)+" / "+std::to_string(total)}});
                auto found=index.find(id);
                if(found==index.end()) throw JudgeFailure{"JE","题目数据损坏：缺少用例 "+id};
                auto runDirectory=directory/"run"/wide(id);
                fs::create_directories(runDirectory);
                auto judgement=judgeCase(program,runDirectory,*found->second,customChecker?&checker:nullptr,timeMs,memoryMb,&cancel);
                cases.push_back({{"caseId",id},{"group",groupName},{"verdict",judgement.verdict},
                                 {"timeMs",judgement.timeMs},{"memoryBytes",judgement.memoryBytes},{"message",judgement.message}});
                ++completed;
                update({{"cases",cases},{"completed",completed}});
                if(judgement.verdict!="AC") {
                    passed=false;
                    if(verdict=="AC") { verdict=judgement.verdict; message=judgement.message; }
                    if(judgement.verdict=="CANCELLED") throw JudgeFailure{"CANCELLED","已停止任务"};
                    break;
                }
            }
            groups[groupIndex]["earned"]=passed?points:0;
            groups[groupIndex]["state"]=passed?"passed":"failed";
            if(passed) score+=points;
            update({{"groups",groups},{"score",score}});
        }
    } catch(const JudgeFailure& failure) {
        verdict=failure.verdict; message=failure.message;
    } catch(const std::exception& e) {
        verdict=cancel.load()?"CANCELLED":"JE"; message=e.what();
    }
    if(verdict=="CE" || verdict=="JE" || verdict=="CANCELLED") {
        // 规格 §4.3：判定/编译级错误不参与计分。
        score=0;
        for(auto& group:groups) { group["earned"]=0; group["state"]="pending"; }
    }
    long long duration=static_cast<long long>(std::chrono::duration_cast<std::chrono::milliseconds>(
        std::chrono::steady_clock::now()-started).count());
    bool improved=previousBest.is_null()?score>0:score>previousBest.get<long long>();
    Json best=previousBest.is_null()?Json(score):Json(std::max(previousBest.get<long long>(),score));
    if(message.empty() || verdict=="AC") {
        long long passedGroups=0;
        for(const auto& group:groups) if(group.value("state",std::string())=="passed") ++passedGroups;
        auto all=static_cast<long long>(groups.size());
        message=verdict=="AC"?"全部 "+std::to_string(all)+" 组通过，得分 "+std::to_string(score)+"/100"
                             :"通过 "+std::to_string(passedGroups)+"/"+std::to_string(all)+" 组，得分 "+std::to_string(score)+"/100";
    }
    auto finishedAt=nowIso();
    update({{"done",true},{"phase","已完成"},{"verdict",verdict},{"score",score},{"best",best},{"improved",improved},
            {"finishedAt",finishedAt},{"message",message},{"groups",groups},{"cases",cases},{"completed",completed}});
    Json record={{"id",submissionId},{"problemId",problemId},{"language",language},{"source",source},
                 {"verdict",verdict},{"score",score},{"cases",cases},{"groups",groups},{"compileLog",compileLog},
                 {"at",startedAt},{"durationMs",duration},{"message",message},{"improved",improved},
                 {"previousBest",previousBest}};
    if(record.dump(2).size()>256*1024) {
        record["compileLog"]="";
        if(record.at("source").get_ref<const std::string&>().size()>120*1024) {
            auto clipped=record.at("source").get<std::string>();
            clipped.resize(120*1024);
            record["source"]=clipped;
            record["sourceTruncated"]=true;
        }
    }
    try { saveSubmission(cacheRoot,record); }
    catch(const std::exception& e) {
        update({{"message",message+"（提交记录保存失败："+std::string(e.what())+"）"}});
    }
}

namespace {
std::string hex64(std::string_view a,std::string_view b,std::string_view c,std::string_view d) {
    std::uint64_t hash=1469598103934665603ULL;
    for(auto part:{a,b,c,d}) { for(unsigned char ch:part) { hash^=ch; hash*=1099511628211ULL; } hash^=0xff; hash*=1099511628211ULL; }
    char key[17]; std::snprintf(key,sizeof key,"%016llx",static_cast<unsigned long long>(hash));
    return key;
}
std::string clip(std::string text,std::size_t limit,bool& truncated) {
    truncated=text.size()>limit;
    if(truncated) { text.resize(limit); while(!text.empty() && (static_cast<unsigned char>(text.back())&0xC0)==0x80) text.pop_back(); }
    return text;
}
Json programToJson(const Program& p) {
    Json env=Json::array(),paths=Json::array(),args=Json::array();
    for(const auto& [k,v]:p.environment) env.push_back({utf8(k),utf8(v)});
    for(const auto& x:p.pathEntries) paths.push_back(utf8(x));
    for(const auto& x:p.args) args.push_back(utf8(x));
    return {{"exe",utf8(p.exe)},{"args",args},{"pathEntries",paths},{"environment",env}};
}
Program programFromJson(const Json& j) {
    Program p; p.exe=wide(j.at("exe").get<std::string>());
    for(const auto& x:j.at("args")) p.args.push_back(wide(x.get<std::string>()));
    for(const auto& x:j.at("pathEntries")) p.pathEntries.push_back(wide(x.get<std::string>()));
    for(const auto& x:j.at("environment")) p.environment.emplace_back(wide(x.at(0).get<std::string>()),wide(x.at(1).get<std::string>()));
    return p;
}
}

// 题目自测：与正式提交走同一套组装 / 编译（driver + 选手代码），输入由用户给，期望输出可选（交本题 checker 比较）。
// 同步执行；不写提交记录、不影响 best。编译产物按「题目版本 + 语言 + 源码 + driver」缓存，只改输入时不重新编译。
Json runCustomTests(const fs::path& cacheRoot,const fs::path& dataDir,const Json& tools,const std::string& problemId,const Json& request) {
    static const std::string allowed="abcdefghijklmnopqrstuvwxyz0123456789-";
    if(problemId.size()<2 || problemId.size()>48 || problemId.find_first_not_of(allowed)!=std::string::npos) throw ApiError(404,"题目不存在");
    auto meta=problemMeta(problemId);
    auto language=request.value("language",std::string());
    auto source=request.value("source",std::string());
    if(language!="cpp" && language!="cangjie") throw ApiError(400,"language 只能是 cpp 或 cangjie");
    if(source.empty()) throw ApiError(400,"源码为空");
    if(source.size()>1024*1024) throw ApiError(400,"源码超过 1 MiB");
    auto tests=request.value("tests",Json::array());
    if(!tests.is_array() || tests.empty()) throw ApiError(400,"至少需要一组自测输入");
    if(tests.size()>10) throw ApiError(400,"自测最多 10 组");
    bool functionMode=meta.value("judgeMode",std::string())=="function";
    auto function=meta.value("function",Json::object());
    std::string driver;
    if(functionMode) {
        if(!function.value("drivers",Json::object()).contains(language)) throw ApiError(400,"本题没有提供该语言的 driver");
        driver=function.at("drivers").at(language).get<std::string>();
    }
    auto limits=meta.value("limits",Json::object());
    long long timeMs=limits.value("timeMs",2000LL),memoryMb=limits.value("memoryMb",512LL);

    auto root=cacheRoot/L".cache"/L"selftest";
    auto key=hex64(problemId+"\n"+meta.value("storedAt",std::string()),language,source,driver);
    auto buildDirectory=root/wide(key);
    auto manifest=buildDirectory/L"program.json";
    Json out={{"compile",{{"ok",true},{"cached",false},{"log",""},{"verdict","AC"},{"message",""},{"ms",0}}},{"results",Json::array()}};
    Program program;
    std::error_code ec;
    bool cached=false;
    if(fs::is_regular_file(manifest)) {
        try { program=programFromJson(Json::parse(readFile(manifest))); cached=fs::is_regular_file(fs::path(program.exe)); } catch(...) { cached=false; }
    }
    if(!cached) {
        // 只保留最近几份产物，避免 .cache 无限增长（checker-build / run 是固定目录，不计入）。
        std::vector<fs::directory_entry> old;
        if(fs::is_directory(root,ec))
            for(const auto& entry:fs::directory_iterator(root,ec))
                if(entry.is_directory() && entry.path().filename().wstring().size()==16) old.push_back(entry);
        std::sort(old.begin(),old.end(),[](const auto& a,const auto& b){ return a.last_write_time()>b.last_write_time(); });
        for(std::size_t i=3;i<old.size();++i) fs::remove_all(old[i].path(),ec);
        fs::remove_all(buildDirectory,ec);
        fs::create_directories(buildDirectory);
        auto started=std::chrono::steady_clock::now();
        if(functionMode) {
            if(language=="cpp") program=buildUnit(language,{{"Main.cpp",assembleCpp(driver,{source})}},buildDirectory,tools,nullptr);
            else program=buildUnit(language,assembleCangjie(driver,function.value("package",std::string()),{source},true),buildDirectory,tools,nullptr);
        } else program=compileProgram(source,language,buildDirectory,tools,nullptr);
        out["compile"]["ms"]=std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now()-started).count();
        bool truncated=false;
        out["compile"]["log"]=clip(program.log,64*1024,truncated);
        if(program.verdict!="AC") {
            out["compile"]["ok"]=false; out["compile"]["verdict"]=program.verdict; out["compile"]["message"]=program.message;
            fs::remove_all(buildDirectory,ec);
            return out;
        }
        writeFile(manifest,programToJson(program).dump());
    }
    out["compile"]["cached"]=cached;
    std::string checkerSource=meta.value("checker",std::string());
    bool needChecker=false;
    for(const auto& t:tests) if(!trim(t.value("expected",std::string())).empty()) needChecker=true;
    Program checker;
    if(needChecker && !checkerSource.empty()) {
        auto checkerDirectory=root/L"checker-build";
        fs::remove_all(checkerDirectory,ec);
        fs::create_directories(checkerDirectory);
        writeFile(checkerDirectory/L"testlib.h",testlib_asset::header);
        checker=buildChecker(meta.value("checker",std::string()),checkerDirectory,tools,nullptr);
        if(checker.verdict!="AC") throw ApiError(500,"checker 编译失败："+firstLines(checker.log,20));
    }
    auto runRoot=root/L"run";
    fs::remove_all(runRoot,ec);
    int index=0;
    for(const auto& t:tests) {
        auto directory=runRoot/std::to_wstring(index++);
        fs::create_directories(directory);
        auto input=t.value("input",std::string());
        if(input.size()>4*1024*1024) throw ApiError(400,"单组输入超过 4 MiB");
        if(!input.empty() && input.back()!='\n') input+='\n';
        auto expected=t.value("expected",std::string());
        writeFile(directory/L"input.txt",input);
        RunOptions options;
        options.timeMs=timeMs;
        options.memoryBytes=static_cast<std::uint64_t>(memoryMb)*1024*1024;
        options.outputBytes=std::max<std::size_t>(1024*1024,expected.size()+1024*1024);
        options.workingDirectory=directory.wstring();
        options.inputPath=(directory/L"input.txt").wstring();
        options.stdoutPath=(directory/L"out.txt").wstring();
        options.pathEntries=program.pathEntries;
        options.environment=program.environment;
        auto run=runProcess(program.exe,program.args,"",options);
        Json item={{"timeMs",run.runTimeMs},{"memoryBytes",run.runMemory},{"exitCode",run.exit},{"message",""}};
        std::string stdoutText;
        try { if(fs::is_regular_file(directory/L"out.txt")) stdoutText=readFile(directory/L"out.txt"); } catch(...) {}
        bool truncated=false;
        item["stdout"]=clip(stdoutText,64*1024,truncated); item["stdoutTruncated"]=truncated;
        item["stderr"]=clip(run.errOut,8*1024,truncated);
        std::string verdict;
        if(!run.started || !run.errorMessage.empty()) { verdict="JE"; item["message"]="运行失败："+run.errorMessage; }
        else if(run.MLE) { verdict="MLE"; item["message"]="超过内存限制 "+std::to_string(memoryMb)+" MiB"; }
        else if(run.OLE) { verdict="OLE"; item["message"]="输出超过限制"; }
        else if(run.TLE) { verdict="TLE"; item["message"]="超过时间限制 "+std::to_string(timeMs)+" ms"; }
        else if(run.exit) { verdict="RE"; item["message"]="程序退出码："+std::to_string(run.exit); }
        else if(trim(expected).empty()) verdict="OK";
        else {
            writeFile(directory/L"answer.txt",expected);
            if(checkerSource.empty()) {
                // 题包没有 checker.cpp：按 token 比较
                auto comparison=compareOutputFiles(directory/L"out.txt",directory/L"answer.txt","tokens",1e-6);
                if(comparison.equal) verdict="AC";
                else { verdict="WA"; item["message"]=clip(trim(comparison.message),4096,truncated); }
            } else {
            RunOptions checkOptions;
            checkOptions.timeMs=10000; checkOptions.memoryBytes=512ULL*1024*1024; checkOptions.outputBytes=32*1024;
            checkOptions.workingDirectory=directory.wstring();
            checkOptions.pathEntries=checker.pathEntries; checkOptions.environment=checker.environment;
            auto check=runProcess(checker.exe,{(directory/L"input.txt").wstring(),(directory/L"out.txt").wstring(),(directory/L"answer.txt").wstring()},"",checkOptions);
            if(!check.started || !check.errorMessage.empty() || check.TLE || check.MLE || check.OLE) { verdict="JE"; item["message"]="checker 运行失败（期望输出可能不符合本题的输出格式）"; }
            else if(check.exit==0) verdict="AC";
            else { verdict="WA"; item["message"]=clip(trim(check.stdOut+check.errOut),4096,truncated); }
            }
        }
        item["verdict"]=verdict;
        out["results"].push_back(item);
    }
    return out;
}
