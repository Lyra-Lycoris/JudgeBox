#include "compiler.hpp"
#include "path_compat.hpp"
#include <optional>
#include <regex>
#include <sstream>

namespace {
std::string findTool(const wchar_t* name,const std::vector<fs::path>& fallbacks={}) {
    wchar_t buffer[32768]; DWORD n=SearchPathW(nullptr,name,L".exe",32768,buffer,nullptr);
    if(n && n<32768 && fs::is_regular_file(buffer)) return utf8(buffer);
    for(const auto& p:fallbacks) if(fs::is_regular_file(p)) return utf8(p.wstring());
    return "";
}
}
const std::vector<std::pair<std::string,fs::path>>& runtimeLayout() {
    static const std::vector<std::pair<std::string,fs::path>> layout={
        {"cpp",L"gcc/bin/g++.exe"},{"python",L"python/python.exe"},{"java",L"jdk/bin/java.exe"},
        {"javac",L"jdk/bin/javac.exe"},{"cangjie",L"cangjie/bin/cjc.exe"}};
    return layout;
}
fs::path runtimeDirectory(const fs::path& applicationDirectory) {
    auto accept=[&](const fs::path& path)->fs::path{
        std::error_code ec;
        if(!fs::is_directory(path,ec)) return {};
        return asciiDirectory(path);
    };
    if(auto direct=accept(applicationDirectory/L"runtimes"); !direct.empty()) return direct;
    if(auto staged=accept(applicationDirectory/L".runtime/stage/JudgeBox/runtimes"); !staged.empty()) return staged;
    return accept(applicationDirectory.parent_path()/L".runtime/stage/JudgeBox/runtimes");
}
Json bundledTools(const fs::path& applicationDirectory) {
    Json tools=Json::object();
    auto runtime=runtimeDirectory(applicationDirectory);
    for(const auto& [key,path]:runtimeLayout()) {
        auto candidate=runtime.empty()?fs::path():runtime/path;
        tools[key]=!candidate.empty() && fs::is_regular_file(candidate)?utf8(candidate.wstring()):"";
    }
    return tools;
}
Json detectTools(const fs::path& applicationDirectory) {
    auto runtime=runtimeDirectory(applicationDirectory);
    Json tools=bundledTools(applicationDirectory);
    if(!runtime.empty() && fs::is_regular_file(runtime/L"manifest.json")) return tools;
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

namespace {
struct Mark { int line=0,column=0,endLine=0,endColumn=0; std::string severity,message; };
std::string lowerCopy(std::string s) { for(char& c:s) c=static_cast<char>(std::tolower(static_cast<unsigned char>(c))); return s; }
Json markJson(Mark m) {
    if(m.line<1) m.line=1;
    if(m.column<1) m.column=1;
    if(m.endLine<m.line) m.endLine=m.line;
    if(m.endLine==m.line && m.endColumn<=m.column) m.endColumn=m.column+1;
    return {{"line",m.line},{"column",m.column},{"endLine",m.endLine},{"endColumn",m.endColumn},{"severity",m.severity=="warning"?"warning":"error"},{"message",m.message}};
}
std::vector<Mark> parseCompilerLog(const std::string& log) {
    std::regex located(R"(:(\d+):(?:(\d+):)?[ \t]*(fatal error|error|warning):[ \t]*(.*)$)",std::regex::icase);
    std::regex bare(R"(^[ \t]*(error|warning):[ \t]*(.*)$)",std::regex::icase);
    std::regex arrow(R"(==>.*:(\d+):(\d+):[ \t]*$)");
    std::regex pipeLine(R"(^[ \t]*\|(.*)$)");
    std::vector<Mark> marks; std::optional<Mark> pending; int open=-1;
    auto closePending=[&]() {
        if(!pending || pending->message.empty()) { pending.reset(); return; }
        marks.push_back(*pending); pending.reset(); open=static_cast<int>(marks.size())-1; if(marks.size()>=40) return;
    };
    std::istringstream lines(log); std::string line;
    while(std::getline(lines,line) && marks.size()<40) {
        if(!line.empty() && line.back()=='\r') line.pop_back();
        std::smatch found;
        if(std::regex_search(line,found,located)) {
            closePending(); if(marks.size()>=40) break;
            Mark mark; mark.line=std::stoi(found[1]); mark.column=found[2].matched?std::stoi(found[2]):0;
            mark.severity=lowerCopy(found[3])=="warning"?"warning":"error"; mark.message=found[4];
            if(mark.severity=="error" && lowerCopy(found[3]).find("fatal")!=std::string::npos) mark.severity="error";
            marks.push_back(mark); open=static_cast<int>(marks.size())-1; continue;
        }
        if(pending && std::regex_search(line,found,arrow)) {
            pending->line=std::stoi(found[1]); pending->column=std::stoi(found[2]); closePending(); continue;
        }
        if(std::regex_search(line,found,bare)) { closePending(); pending=Mark{}; pending->severity=lowerCopy(found[1])=="warning"?"warning":"error"; pending->message=found[2]; open=-1; continue; }
        std::smatch frame;
        if(open>=0 && std::regex_match(line,frame,pipeLine)) {
            auto body=frame[1].str(); auto hat=body.find('^');
            if(hat!=std::string::npos) {
                int span=0; for(std::size_t i=hat;i<body.size() && (body[i]=='^' || body[i]=='~');++i) ++span;
                auto& mark=marks[open];
                if(mark.column<=0) mark.column=static_cast<int>(hat)+1;
                if(span>0 && mark.column>0) mark.endColumn=mark.column+span;
            }
            continue;
        }
        auto hat=line.find('^'); if(hat==std::string::npos || open<0) continue;
        if(line.find_first_not_of(" \t|^~0123456789")!=std::string::npos) continue;
        int tildes=0; for(std::size_t i=hat+1;i<line.size() && line[i]=='~';++i) ++tildes;
        auto& mark=marks[open];
        if(mark.column<=0 && line.find('|')==std::string::npos) mark.column=static_cast<int>(hat)+1;
        if(mark.column>0) mark.endColumn=mark.column+1+tildes;
    }
    closePending(); if(marks.size()>40) marks.resize(40); return marks;
}
std::string languageName(const std::string& language) {
    if(language=="cpp") return "C++";
    if(language=="python") return "Python";
    if(language=="java") return "Java";
    if(language=="cangjie") return "仓颉";
    return language;
}
}
Json diagnoseSource(const std::string& source,const std::string& language,const Json& tools,const fs::path& workspace) {
    Json empty={{"diagnostics",Json::array()},{"status",""}};
    if(language!="cpp" && language!="python" && language!="java" && language!="cangjie") return {{"diagnostics",Json::array()},{"status","不支持的语言"}};
    if(source.size()>1024*1024) return {{"diagnostics",Json::array()},{"status","源码超过 1 MiB，已跳过检查"}};
    if(source.empty()) return empty;
    auto compiler=tools.value(language=="java"?"javac":language,std::string());
    if(compiler.empty() || !fs::is_regular_file(fs::path(wide(compiler)))) return {{"diagnostics",Json::array()},{"status","安装目录中没有"+languageName(language)+"工具链，语言服务不可用"}};
    fs::create_directories(workspace);
    auto dir=workspace/("lint-"+std::to_string(GetTickCount64()));
    struct Cleanup { fs::path path; ~Cleanup(){ std::error_code ec; fs::remove_all(path,ec); } } cleanup{dir};
    fs::create_directories(dir);
    fs::path compilerPath=fs::path(wide(compiler));
    wchar_t compilerShortName[32768]; DWORD compilerShortLength=GetShortPathNameW(compilerPath.c_str(),compilerShortName,32768);
    if(compilerShortLength && compilerShortLength<32768) compilerPath=compilerShortName;
    if(language=="cpp" || language=="cangjie") {
        auto parent=compilerPath.parent_path();
        if(parent.filename()==L"bin") compilerPath=asciiDirectory(parent.parent_path())/L"bin"/compilerPath.filename();
        else compilerPath=asciiDirectory(parent)/compilerPath.filename();
    }
    RunOptions opt; opt.timeMs=8000; opt.memoryBytes=512ULL*1024*1024; opt.outputBytes=256*1024;
    opt.pathEntries.push_back(compilerPath.parent_path().wstring());
    if(language=="java") for(const auto* key:{L"JAVA_TOOL_OPTIONS",L"JDK_JAVA_OPTIONS",L"_JAVA_OPTIONS",L"CLASSPATH"}) opt.environment.emplace_back(key,L"");
    if(language=="cpp") for(const auto* key:{L"GCC_EXEC_PREFIX",L"COMPILER_PATH",L"LIBRARY_PATH",L"CPATH",L"CPLUS_INCLUDE_PATH",L"C_INCLUDE_PATH"}) opt.environment.emplace_back(key,L"");
    if(language=="cangjie") {
        auto home=compilerPath.parent_path().parent_path(); opt.environment.emplace_back(L"CANGJIE_HOME",home.wstring());
        for(const auto& part:{L"runtime/lib/windows_x86_64_cjnative",L"lib/windows_x86_64_cjnative",L"tools/bin",L"tools/lib"}) opt.pathEntries.push_back((home/part).wstring());
        opt.workingDirectory=asciiDirectory(dir).wstring();
    } else opt.workingDirectory=dir.wstring();
    std::vector<std::wstring> args; std::string input;
    if(language=="python") {
        writeFile(dir/"check.py",R"PY(import ast, json, sys
source = sys.stdin.read()
items = []
try:
    ast.parse(source)
except SyntaxError as error:
    line = error.lineno or 1
    column = error.offset or 1
    end_line = error.end_lineno or line
    end_column = error.end_offset or 0
    if end_line < line: end_line = line
    if end_line == line and end_column <= column: end_column = column + 1
    items.append({"line": line, "column": column, "endLine": end_line, "endColumn": end_column, "severity": "error", "message": error.msg or "语法错误"})
json.dump({"diagnostics": items}, sys.stdout, ensure_ascii=False)
)PY");
        args={L"-X",L"utf8",(dir/"check.py").wstring()}; input=source;
    } else if(language=="cpp") {
        writeFile(dir/"Main.cpp",source);
        args={L"-std=c++20",L"-fsyntax-only",L"-fdiagnostics-color=never",L"-finput-charset=UTF-8",L"-fdiagnostics-column-unit=display",L"Main.cpp"};
    } else if(language=="java") {
        writeFile(dir/"Main.java",source);
        args={L"-J-Duser.language=en",L"-J-Duser.country=US",L"-encoding",L"UTF-8",L"-d",L".",L"Main.java"};
    } else {
        writeFile(dir/"main.cj",source);
        args={L"main.cj",L"-o",L"Main.exe",L"--diagnostic-format",L"noColor"};
    }
    auto result=runProcess(compilerPath.wstring(),args,input,opt);
    if(result.cancelled) return {{"diagnostics",Json::array()},{"status","检查已取消"}};
    if(!result.started || !result.errorMessage.empty()) return {{"diagnostics",Json::array()},{"status","无法启动"+languageName(language)+"检查："+result.errorMessage}};
    if(result.TLE || result.MLE || result.OLE) return {{"diagnostics",Json::array()},{"status",languageName(language)+"检查超时或超出资源限制"}};
    if(language=="python") {
        try { auto parsed=Json::parse(result.stdOut); if(parsed.is_object() && parsed.contains("diagnostics") && parsed.at("diagnostics").is_array()) return {{"diagnostics",parsed.at("diagnostics")},{"status",""}}; }
        catch(...) {}
        auto message=result.errOut.empty()?result.stdOut:result.errOut; if(message.size()>240) message.resize(240);
        return {{"diagnostics",Json::array()},{"status",message.empty()?"Python 检查失败":message}};
    }
    Json diagnostics=Json::array();
    for(const auto& mark:parseCompilerLog(result.stdOut+result.errOut)) diagnostics.push_back(markJson(mark));
    std::string status;
    if(diagnostics.empty() && result.exit) status=languageName(language)+"检查未通过";
    return {{"diagnostics",diagnostics},{"status",status}};
}
