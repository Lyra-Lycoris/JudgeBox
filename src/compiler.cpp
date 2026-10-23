#include "compiler.hpp"
#include "path_compat.hpp"

namespace {
std::string findTool(const wchar_t* name,const std::vector<fs::path>& fallbacks={}) {
    wchar_t buffer[32768]; DWORD n=SearchPathW(nullptr,name,L".exe",32768,buffer,nullptr);
    if(n && n<32768 && fs::is_regular_file(buffer)) return utf8(buffer);
    for(const auto& p:fallbacks) if(fs::is_regular_file(p)) return utf8(p.wstring());
    return "";
}
}
Json detectTools(const fs::path& applicationDirectory) {
    auto runtime=applicationDirectory/L"runtimes";
    if(fs::is_directory(runtime)) runtime=asciiDirectory(runtime);
    Json tools=Json::object();
    for(const auto& [key,path]:std::vector<std::pair<std::string,fs::path>>{
        {"cpp",L"gcc/bin/g++.exe"},{"python",L"python/python.exe"},{"java",L"jdk/bin/java.exe"},
        {"javac",L"jdk/bin/javac.exe"},{"cangjie",L"cangjie/bin/cjc.exe"}}) {
        auto candidate=runtime/path; tools[key]=fs::is_regular_file(candidate)?utf8(candidate.wstring()):"";
    }
    if(fs::is_regular_file(runtime/L"manifest.json")) return tools;
    Json installed={{"cpp",findTool(L"g++.exe",{L"C:\\msys64\\ucrt64\\bin\\g++.exe"})},
            {"python",findTool(L"python.exe")},{"java",findTool(L"java.exe")},
            {"javac",findTool(L"javac.exe")},{"cangjie",findTool(L"cjc.exe",{L"D:\\Cangjie\\cangjie\\bin\\cjc.exe"})}};
    for(auto it=tools.begin();it!=tools.end();++it) if(it.value()=="") it.value()=installed.at(it.key());
    return tools;
}
Program compileProgram(const std::string& source,const std::string& language,const fs::path& dir,const Json& tools,const std::atomic_bool* cancel) {
    Program p;
    if(source.empty() || source.size()>1024*1024) { p.verdict="JE"; p.message="源码不能为空，且不能超过 1 MiB"; return p; }
    if(language!="cpp" && language!="python" && language!="java" && language!="cangjie") { p.verdict="JE"; p.message="不支持的语言"; return p; }
    auto compiler=tools.value(language=="java"?"javac":language,std::string());
    if(compiler.empty() || !fs::is_regular_file(fs::path(wide(compiler)))) { p.verdict="JE"; p.message="找不到 "+language+" 编译器/解释器，请在工具链设置填写完整路径"; return p; }
    fs::create_directories(dir);
    fs::path compilerPath=fs::path(wide(compiler));
    wchar_t compilerShortName[32768]; DWORD compilerShortLength=GetShortPathNameW(compilerPath.c_str(),compilerShortName,32768);
    if(compilerShortLength && compilerShortLength<32768) compilerPath=compilerShortName;
    if(language=="cpp" || language=="cangjie") {
        auto parent=compilerPath.parent_path();
        if(parent.filename()==L"bin") compilerPath=asciiDirectory(parent.parent_path())/L"bin"/compilerPath.filename();
        else compilerPath=asciiDirectory(parent)/compilerPath.filename();
    }
    auto compilerBin=compilerPath.parent_path();
    p.pathEntries.push_back(compilerBin.wstring());
    if(language=="java") for(const auto* key:{L"JAVA_TOOL_OPTIONS",L"JDK_JAVA_OPTIONS",L"_JAVA_OPTIONS",L"CLASSPATH"}) p.environment.emplace_back(key,L"");
    if(language=="cpp") for(const auto* key:{L"GCC_EXEC_PREFIX",L"COMPILER_PATH",L"LIBRARY_PATH",L"CPATH",L"CPLUS_INCLUDE_PATH",L"C_INCLUDE_PATH"}) p.environment.emplace_back(key,L"");
    if(language=="cangjie") {
        auto home=compilerBin.parent_path(); p.environment.emplace_back(L"CANGJIE_HOME",home.wstring());
        for(const auto& part:{L"runtime/lib/windows_x86_64_cjnative",L"lib/windows_x86_64_cjnative",L"tools/bin",L"tools/lib"}) p.pathEntries.push_back((home/part).wstring());
    }
    auto src=dir/(language=="cpp"?"Main.cpp":language=="java"?"Main.java":language=="python"?"main.py":"main.cj");
    writeFile(src,source); auto binary=dir/"Main.exe";
    std::vector<std::wstring> args;
    if(language=="cpp") args={L"-std=c++20",L"-O2",L"-pipe",L"-no-canonical-prefixes",L"-fdiagnostics-color=never",L"-finput-charset=UTF-8",L"Main.cpp",L"-o",L"Main.exe"};
    if(language=="java") args={L"-J-Dfile.encoding=UTF-8",L"-encoding",L"UTF-8",L"-d",L".",L"Main.java"};
    if(language=="python") args={L"-X",L"utf8",L"-m",L"py_compile",src.wstring()};
    if(language=="cangjie") args={L"main.cj",L"-o",L"Main.exe",L"--diagnostic-format",L"noColor"};
    RunOptions opts; opts.timeMs=60000; opts.memoryBytes=2ULL*1024*1024*1024; opts.outputBytes=2*1024*1024; opts.workingDirectory=dir.wstring(); opts.cancel=cancel;
    opts.pathEntries=p.pathEntries; opts.environment=p.environment;
    if(language=="cangjie") {
        opts.workingDirectory=asciiDirectory(dir).wstring();
    }
    auto result=runProcess(compilerPath.wstring(),args,"",opts);
    p.log=result.stdOut+result.errOut;
    if(result.cancelled) { p.verdict="CANCELLED"; p.message="已停止编译"; }
    else if(!result.errorMessage.empty() || !result.started) { p.verdict="JE"; p.message="编译器启动失败："+result.errorMessage; }
    else if(result.TLE || result.MLE || result.OLE) { p.verdict="JE"; p.message="编译器超过资源限制（60 秒 / 2 GiB / 2 MiB 输出）"; }
    else if(result.exit>=0xC0000000UL) { p.verdict="JE"; p.message="编译器异常退出（Windows 状态 "+std::to_string(result.exit)+"），请检查工具链依赖"; }
    else if(result.exit) { p.verdict="CE"; p.message="编译失败，请查看编译日志"; }
    if(p.verdict!="AC") return p;
    p.exe=binary.wstring();
    if(language=="python") { p.exe=wide(compiler); p.args={L"-X",L"utf8",L"-u",src.wstring()}; }
    if(language=="java") {
        auto java=tools.value("java",std::string());
        if(java.empty() || !fs::is_regular_file(fs::path(wide(java)))) { p.verdict="JE"; p.message="找不到 java.exe"; return p; }
        p.exe=wide(java); p.classDirectory=dir; p.java=true;
        p.args={L"-Dfile.encoding=UTF-8",L"-Dstdout.encoding=UTF-8",L"-Dstderr.encoding=UTF-8",L"-Xms16m",L"-Xmx256m",L"-XX:CompressedClassSpaceSize=32m",L"-XX:ReservedCodeCacheSize=32m",L"-cp",L".",L"Main"};
    }
    return p;
}
