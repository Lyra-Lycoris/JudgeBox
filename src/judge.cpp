#include "judge.hpp"
#include "checker.hpp"
#include "dataset.hpp"
#include "generator.hpp"
#include <chrono>

namespace {
long long integer(const Json& obj,const char* key,long long def,long long low,long long high) {
    if(obj.contains(key) && !obj.at(key).is_number_integer()) throw std::runtime_error(std::string(key)+" 必须为整数");
    auto n=obj.value(key,def); if(n<low || n>high) throw std::runtime_error(std::string(key)+" 超出范围 "+std::to_string(low)+".."+std::to_string(high)); return n;
}
std::string safeDump(const Json& j) { return j.dump(2,' ',false,Json::error_handler_t::replace); }
void prepareRuntime(const Program& program,const fs::path& dir) {
    fs::create_directories(dir);
    if(!program.classDirectory.empty()) for(const auto& file:fs::recursive_directory_iterator(program.classDirectory)) {
        if(file.is_regular_file() && file.path().extension()==L".class") {
            auto target=dir/fs::relative(file.path(),program.classDirectory); fs::create_directories(target.parent_path()); fs::copy_file(file.path(),target,fs::copy_options::overwrite_existing);
        }
    }
}
std::vector<std::wstring> runtimeArgs(const Program& program,std::uint64_t memoryBytes) {
    auto args=program.args;
    if(program.java) {
        auto mb=memoryBytes/(1024*1024);
        auto heap=std::max<std::uint64_t>(16,mb>192?mb-128:mb/2);
        for(auto& arg:args) if(arg.starts_with(L"-Xmx")) arg=L"-Xmx"+std::to_wstring(heap)+L"m";
    }
    return args;
}
std::string verdict(const runResult& r) {
    if(r.cancelled) return "CANCELLED";
    if(!r.errorMessage.empty() || !r.started) return "JE";
    if(r.MLE) return "MLE";
    if(r.OLE) return "OLE";
    if(r.TLE) return "TLE";
    return r.exit?"RE":"RUN";
}
std::string reason(const runResult& r) {
    if(!r.errorMessage.empty()) return r.errorMessage;
    if(r.MLE) return "触发 Windows 作业提交内存硬上限";
    if(r.OLE) return "stdout 和 stderr 总量超过输出限制";
    if(r.TLE) return "超过墙钟时间限制，已终止进程树";
    if(r.cancelled) return "已停止";
    if(r.exit) return "程序退出码："+std::to_string(r.exit);
    return "未提供预期输出，仅展示运行结果";
}
Json toolsFor(const Json& request,const Json& defaults) {
    Json tools=defaults;
    if(request.contains("tools")) {
        if(!request.at("tools").is_object()) throw std::runtime_error("tools 必须为对象");
        for(auto it=request.at("tools").begin();it!=request.at("tools").end();++it) if(tools.contains(it.key()) && it.value().is_string() && !it.value().get<std::string>().empty()) tools[it.key()]=it.value();
    }
    return tools;
}
std::string generate(const Json& request,const Json& tools,std::uint64_t seed,int index,const fs::path& dir,const std::atomic_bool* cancel) {
    if(request.value("generatorMode",std::string("rules"))!="python") return generateInput(request.at("generator"),seed,index,request.value("strategy",std::string("random")));
    auto python=tools.value("python",std::string()); if(python.empty()) throw std::runtime_error("Python 生成器需要配置 python.exe");
    fs::create_directories(dir); auto script=dir/"generator.py";
    auto source=request.value("generatorSource",std::string()); if(source.empty() || source.size()>1024*1024) throw std::runtime_error("生成器源码不能为空或超过 1 MiB");
    writeFile(script,source);
    RunOptions opt; opt.timeMs=5000; opt.memoryBytes=256*1024*1024; opt.outputBytes=1024*1024; opt.cancel=cancel; opt.workingDirectory=dir.wstring();
    auto r=runProcess(wide(python),{L"-X",L"utf8",L"-u",script.wstring(),std::to_wstring(seed),std::to_wstring(index)},"",opt);
    if(verdict(r)!="RUN") throw std::runtime_error("生成器失败："+reason(r)+"\n"+r.errOut);
    return r.stdOut;
}
}
JudgeEngine::JudgeEngine(fs::path path,Json tools):root(std::move(path)),defaultTools(std::move(tools)) {
    fs::create_directories(root);
    state={{"done",true},{"verdict","READY"},{"phase","就绪"},{"message",""},{"cases",Json::array()},{"completed",0},{"total",0},{"compileLog",""}};
}
JudgeEngine::~JudgeEngine() { stop(); if(worker.joinable()) worker.join(); }
void JudgeEngine::update(const Json& fields) { std::lock_guard lock(mutex); state.update(fields); }
Json JudgeEngine::status() { std::lock_guard lock(mutex); return state; }
void JudgeEngine::stop() { cancel=true; }
Json JudgeEngine::start(const Json& request) {
    { std::lock_guard lock(mutex); if(!state.at("done").get<bool>()) throw std::runtime_error("已有任务正在运行"); }
    auto mode=request.value("mode",std::string("manual"));
    if(mode!="manual" && mode!="generated" && mode!="stress") throw std::runtime_error("无效运行模式");
    if(request.value("source",std::string()).empty()) throw std::runtime_error("请粘贴待测源码");
    if(mode=="stress" && request.value("reference",std::string()).empty()) throw std::runtime_error("请粘贴参考程序");
    integer(request,"timeMs",1000,10,60000); integer(request,"memoryMb",256,16,4096); integer(request,"outputKb",1024,1,16*1024*1024);
    integer(request,"seed",42,0,9007199254740991LL);
    const bool datasetMode=request.contains("dataset");
    std::size_t total=0;
    if(datasetMode) {
        if(mode!="manual" || !request.at("dataset").is_object() || !request.at("dataset").value("directory",std::string()).size()) throw std::runtime_error("数据目录参数不正确");
        total=loadDataset(request.at("dataset").at("directory").get<std::string>()).cases.size();
    } else if(mode=="manual") {
        if(!request.contains("cases") || !request.at("cases").is_array() || request.at("cases").empty() || request.at("cases").size()>200) throw std::runtime_error("请提供 1..200 组测试点");
        for(const auto& c:request.at("cases")) if(!c.at("input").is_string() || c.at("input").get_ref<const std::string&>().size()>1024*1024 || (c.contains("expected") && !c.at("expected").is_null() && !c.at("expected").is_string())) throw std::runtime_error("测试输入须为文本且不超过 1 MiB；答案须为文本或 null");
        total=request.at("cases").size();
    } else { integer(request,"count",20,1,1000); total=static_cast<std::size_t>(request.value("count",20)); }
    compareOutput("","",request.value("checker",std::string("tokens")),request.value("tolerance",1e-6));
    if(worker.joinable()) worker.join();
    auto now=std::chrono::system_clock::now().time_since_epoch();
    current=root/(std::to_string(std::chrono::duration_cast<std::chrono::milliseconds>(now).count())+"-"+std::to_string(GetTickCount64()));
    fs::create_directories(current); writeFile(current/"request.json",safeDump(request));
    cancel=false;
    update({{"done",false},{"verdict","RUNNING"},{"phase","准备编译"},{"message",""},{"cases",Json::array()},{"completed",0},{"total",total},{"compileLog",""},{"directory",utf8(current.wstring())},{"seed",request.value("seed",42LL)}});
    worker=std::thread(&JudgeEngine::execute,this,request,current);
    return {{"ok",true}};
}
Json JudgeEngine::detail(int index) {
    std::lock_guard lock(mutex);
    if(index<0 || static_cast<std::size_t>(index)>=state.at("cases").size()) throw std::runtime_error("测试点不存在");
    auto detail=Json::parse(readFile(current/("case-"+std::to_string(index)+".json")));
    if(detail.value("fileBacked",false)) {
        for(const char* key:{"input","expected","stdout"}) {
            std::string pathKey=std::string(key)+"Path";
            if(detail.at(pathKey).is_string()) {
                auto path=fs::path(wide(detail.at(pathKey).get<std::string>()));
                detail[key]=readFilePreview(path);
                detail[std::string(key)+"Truncated"]=fs::file_size(path)>detail.at(key).get_ref<const std::string&>().size();
            } else detail[key]=nullptr;
        }
    }
    return detail;
}
Json JudgeEngine::preview(const Json& request) {
    auto seed=integer(request,"seed",42,0,9007199254740991LL); auto index=integer(request,"index",0,0,999);
    auto tools=toolsFor(request,defaultTools);
    auto dir=root/("preview-"+std::to_string(GetTickCount64()));
    return {{"input",generate(request,tools,seed,static_cast<int>(index),dir,nullptr)},{"seed",seed},{"index",index}};
}
void JudgeEngine::execute(Json request,fs::path directory) {
    std::string overall="AC",message;
    try {
        auto tools=toolsFor(request,defaultTools);
        auto program=compileProgram(request.at("source"),request.value("language",std::string("cpp")),directory/"submission",tools,&cancel);
        update({{"compileLog",program.log}});
        if(program.verdict!="AC") { overall=program.verdict; message=program.message; }
        else {
            Program reference; auto mode=request.value("mode",std::string("manual"));
            const bool datasetMode=request.contains("dataset");
            Dataset dataset;
            if(datasetMode) dataset=loadDataset(request.at("dataset").at("directory").get<std::string>());
            if(mode=="stress") {
                update({{"phase","编译参考程序"}});
                reference=compileProgram(request.at("reference"),request.value("referenceLanguage",std::string("cpp")),directory/"reference",tools,&cancel);
                update({{"compileLog",program.log+"\n[参考程序]\n"+reference.log}});
                if(reference.verdict!="AC") { overall=reference.verdict=="CANCELLED"?"CANCELLED":"JE"; message="参考程序 "+reference.verdict+"："+reference.message; }
            }
            RunOptions opts; opts.cancel=&cancel; opts.timeMs=request.value("timeMs",1000LL); opts.memoryBytes=request.value("memoryMb",256ULL)*1024*1024; opts.outputBytes=request.value("outputKb",1024ULL)*1024;
            if(datasetMode) opts.outputBytes=std::max(opts.outputBytes,static_cast<std::size_t>(dataset.maxExpectedBytes+1024*1024));
            int total=datasetMode?static_cast<int>(dataset.cases.size()):mode=="manual"?static_cast<int>(request.at("cases").size()):request.value("count",20);
            bool noAnswer=false;
            for(int i=0;i<total && overall!="JE" && overall!="CANCELLED";++i) {
                if(cancel.load()) { overall="CANCELLED"; message="已停止"; break; }
                update({{"phase","运行测试点 "+std::to_string(i+1)+" / "+std::to_string(total)}});
                auto caseDir=directory/("test-"+std::to_string(i+1)); fs::create_directories(caseDir);
                const DatasetCase* test=datasetMode?&dataset.cases[i]:nullptr;
                std::string input=datasetMode?std::string():mode=="manual"?request.at("cases").at(i).at("input").get<std::string>():generate(request,tools,request.value("seed",42ULL),i,caseDir/"generator",&cancel);
                Json expected=nullptr; runResult refRun;
                if(mode=="manual" && !datasetMode) expected=request.at("cases").at(i).value("expected",Json(nullptr));
                if(mode=="stress") {
                    prepareRuntime(reference,caseDir/"reference"); auto refOpt=opts; refOpt.workingDirectory=(caseDir/"reference").wstring();
                    refOpt.pathEntries=reference.pathEntries; refOpt.environment=reference.environment;
                    refOpt.timeMs=request.value("referenceTimeMs",std::max(5000LL,opts.timeMs));
                    if(refOpt.timeMs<10 || refOpt.timeMs>60000) throw std::runtime_error("参考程序时间上限为 10..60000 ms");
                    refRun=runProcess(reference.exe,runtimeArgs(reference,refOpt.memoryBytes),input,refOpt);
                    if(verdict(refRun)!="RUN") {
                        overall=refRun.cancelled?"CANCELLED":"JE"; message="参考程序 "+verdict(refRun)+"："+reason(refRun);
                        Json detail={{"input",input},{"expected",nullptr},{"stdout",""},{"stderr",refRun.errOut},{"referenceStdout",refRun.stdOut},{"verdict",overall},{"message",message},{"index",i},{"timeMs",refRun.runTimeMs},{"memoryBytes",refRun.runMemory}};
                        writeFile(directory/("case-"+std::to_string(i)+".json"),safeDump(detail));
                        std::lock_guard lock(mutex); state["cases"].push_back({{"index",i},{"verdict",overall},{"message",message},{"timeMs",refRun.runTimeMs},{"memoryBytes",refRun.runMemory}}); state["completed"]=i+1;
                        break;
                    }
                    expected=refRun.stdOut;
                }
                prepareRuntime(program,caseDir/"submission");
                auto runOpts=opts; runOpts.workingDirectory=(caseDir/"submission").wstring();
                runOpts.pathEntries=program.pathEntries; runOpts.environment=program.environment;
                auto stdoutPath=caseDir/"stdout.txt";
                if(test) { runOpts.inputPath=test->input.wstring(); runOpts.stdoutPath=stdoutPath.wstring(); }
                auto run=runProcess(program.exe,runtimeArgs(program,runOpts.memoryBytes),input,runOpts); auto v=verdict(run); auto why=reason(run);
                auto checker=request.value("checker",std::string("tokens")); auto tolerance=request.value("tolerance",1e-6);
                if(v=="RUN" && test && !test->expected.empty()) { auto c=compareOutputFiles(stdoutPath,test->expected,checker,tolerance); v=c.equal?"AC":"WA"; why=c.message; }
                else if(v=="RUN" && !expected.is_null()) { auto c=compareOutput(run.stdOut,expected.get<std::string>(),checker,tolerance); v=c.equal?"AC":"WA"; why=c.message; }
                if(v=="RUN") noAnswer=true;
                Json row={{"index",i},{"verdict",v},{"timeMs",run.runTimeMs},{"memoryBytes",run.runMemory},{"message",why}};
                if(test) row["name"]=test->name;
                Json detail=row;
                if(test) detail.update({{"fileBacked",true},{"inputPath",utf8(test->input.wstring())},{"expectedPath",test->expected.empty()?Json(nullptr):Json(utf8(test->expected.wstring()))},{"stdoutPath",utf8(stdoutPath.wstring())},{"stderr",run.errOut},{"exitCode",run.exit}});
                else detail.update({{"input",input},{"expected",expected},{"stdout",run.stdOut},{"stderr",run.errOut},{"exitCode",run.exit},{"seed",request.value("seed",42ULL)}});
                if(mode=="stress") detail.update({{"referenceTimeMs",refRun.runTimeMs},{"referenceStderr",refRun.errOut}});
                writeFile(directory/("case-"+std::to_string(i)+".json"),safeDump(detail));
                { std::lock_guard lock(mutex); state["cases"].push_back(row); state["completed"]=i+1; }
                if(v!="AC" && v!="RUN") { if(overall=="AC") { overall=v; message=why; } if(mode=="stress" || request.value("stopOnFailure",false) || v=="CANCELLED" || v=="JE") break; }
            }
            if(overall=="AC" && noAnswer) overall="RUN";
        }
    } catch(const std::exception& e) { overall=cancel.load()?"CANCELLED":"JE"; message=e.what(); }
    if(cancel.load()) { overall="CANCELLED"; message="已停止任务"; }
    if(message.empty()) message=overall=="AC"?"全部测试点通过":overall=="RUN"?"运行完成；无预期答案的测试点未判定正确性":"任务结束";
    update({{"verdict",overall},{"message",message},{"phase","已完成"}});
    try { auto summary=status(); summary["done"]=true; writeFile(directory/"result.json",safeDump(summary)); }
    catch(const std::exception& e) { update({{"verdict","JE"},{"message",e.what()}}); }
    update({{"done",true}});
}
