#include "records.hpp"
#include "apierror.hpp"
#include "problems.hpp"
#include <algorithm>
#include <cstdlib>

namespace {
// 目录名里不能出现 Windows 保留字符；中文可以保留（资源管理器与 GitHub 都没问题）。
std::string sanitize(const std::string& text,std::size_t limit) {
    std::string out;
    std::size_t count=0;
    for(std::size_t i=0;i<text.size();++i) {
        unsigned char c=static_cast<unsigned char>(text[i]);
        bool lead=(c&0xC0)!=0x80;
        if(c<0x80) {
            if(std::string("\\/:*?\"<>|").find(static_cast<char>(c))!=std::string::npos || c<0x20) out+='-';
            else out+=static_cast<char>(c);
        } else out+=static_cast<char>(c);
        if(lead && ++count>=limit) break;
    }
    while(!out.empty() && (out.back()==' ' || out.back()=='.' || out.back()=='-')) out.pop_back();
    if(out.empty()) out="problem";
    return out;
}
std::string titleOf(const Json& meta) {
    auto title=meta.value("title",Json::object());
    std::string text=title.value("zh",std::string());
    if(text.empty()) text=title.value("en",std::string());
    return text;
}
std::string packageOf(const Json& meta) {
    auto function=meta.value("function",Json::object());
    auto name=function.value("package",std::string());
    if(name.empty()) name="judgebox";
    return name;
}
struct Layout {
    const char* code;     // 代码文件相对叶子目录的路径
    bool project;         // 是否需要工程骨架（仓颉 / Java）
};
Layout layoutOf(const std::string& language,const std::string& mode) {
    if(language=="cpp") return {mode=="full"?"main.cpp":"solve.cpp",false};
    if(language=="python") return {mode=="full"?"main.py":"solve.py",false};
    if(language=="cangjie") return {mode=="full"?"src/main.cj":"src/solution.cj",true};
    return {mode=="full"?"src/main/java/Main.java":"src/main/java/Solution.java",true};
}
fs::path problemDirectory(const std::string& problemId) {
    auto meta=problemMeta(problemId);
    auto topic=sanitize(meta.value("topic",std::string("未分类")),60);
    auto title=titleOf(meta);
    auto name=sanitize(problemId+(title.empty()?std::string():"_"+title),80);
    return solveRecordRoot()/wide(topic)/wide(name);
}
void ensureProject(const fs::path& leaf,const std::string& language,const std::string& mode,const Json& meta) {
    auto package=sanitize(packageOf(meta),40);
    std::transform(package.begin(),package.end(),package.begin(),[](unsigned char c){ return static_cast<char>(std::tolower(c)); });
    for(char& c:package) if(!((c>='a'&&c<='z')||(c>='0'&&c<='9')||c=='_')) c='_';
    if(package.empty() || (package[0]>='0' && package[0]<='9')) package="judgebox_"+package;
    if(language=="cangjie") {
        auto manifest=leaf/L"cjpm.toml";
        if(!fs::is_regular_file(manifest))
            writeFile(manifest,"[package]\n  cjc-version = \"1.0.0\"\n  name = \""+package+"\"\n  version = \"1.0.0\"\n  output-type = \"executable\"\n\n[dependencies]\n");
        auto script=leaf/L"build.cmd";
        if(!fs::is_regular_file(script))
            writeFile(script,"@echo off\r\nrem 用仓颉编译器直接构建本目录（没有 cjpm 时也能跑）。\r\nif not exist build mkdir build\r\n"
                             "cjc src\\*.cj -o build\\solve.exe --diagnostic-format noColor || exit /b 1\r\n"
                             "echo build\\solve.exe\r\n");
    } else if(language=="java") {
        auto manifest=leaf/L"pom.xml";
        if(!fs::is_regular_file(manifest))
            writeFile(manifest,"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                "<project xmlns=\"http://maven.apache.org/POM/4.0.0\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd\">\n"
                "  <modelVersion>4.0.0</modelVersion>\n  <groupId>judgebox</groupId>\n  <artifactId>"+package+"</artifactId>\n  <version>1.0.0</version>\n"
                "  <properties>\n    <maven.compiler.source>21</maven.compiler.source>\n    <maven.compiler.target>21</maven.compiler.target>\n    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>\n  </properties>\n"
                "  <build>\n    <finalName>solve</finalName>\n  </build>\n</project>\n");
        auto script=leaf/L"build.cmd";
        if(!fs::is_regular_file(script))
            writeFile(script,"@echo off\r\nrem 用 JDK 直接构建本目录（没有 Maven 时也能跑）。\r\nif not exist build mkdir build\r\n"
                             "javac -encoding UTF-8 -d build src\\main\\java\\*.java || exit /b 1\r\necho build\r\n");
    } else if(language=="cpp") {
        auto script=leaf/L"build.cmd";
        if(!fs::is_regular_file(script))
            writeFile(script,"@echo off\r\nrem 单文件构建：把 main.cpp / solve.cpp 编成 build\\solve.exe。\r\nif not exist build mkdir build\r\n"
                             "g++ -std=c++20 -O2 -pipe "+(std::string(mode=="full"?"main.cpp":"solve.cpp"))+" -o build\\solve.exe || exit /b 1\r\necho build\\solve.exe\r\n");
    }
    if(language=="cpp" || language=="python") {
        auto keep=leaf/L".gitkeep";
        if(!fs::exists(keep) && !fs::exists(leaf/wide(layoutOf(language,mode).code))) writeFile(keep,"");
    }
}
Json leafStatus(const fs::path& leaf,const std::string& language,const std::string& mode) {
    auto layout=layoutOf(language,mode);
    auto code=leaf/wide(layout.code);
    Json item={{"language",language},{"mode",mode},{"file",layout.code},{"exists",fs::is_regular_file(code)}};
    if(fs::is_regular_file(code)) { item["bytes"]=static_cast<long long>(fs::file_size(code)); }
    return item;
}
}

fs::path solveRecordRoot() {
    if(const char* value=std::getenv("JUDGEBOX_SOLVE_RECORD"); value && *value) {
        try { return fs::path(wide(std::string(value))); } catch(...) {}
    }
    return executableDirectory()/L"solveRecord";
}

Json saveSolveRecord(const std::string& problemId,const std::string& language,const std::string& mode,const std::string& source) {
    if(problemId.empty()) throw ApiError(400,"缺少题目 id");
    if(language!="cpp" && language!="cangjie" && language!="python" && language!="java") throw ApiError(400,"语言只能是 cpp、cangjie、python 或 java");
    if(mode!="full" && mode!="function") throw ApiError(400,"提交方式只能是 full 或 function");
    if(source.empty()) throw ApiError(400,"代码为空");
    if(source.size()>1024*1024) throw ApiError(400,"代码超过 1 MiB");
    auto meta=problemMeta(problemId);
    auto leaf=problemDirectory(problemId)/wide(language)/wide(mode);
    fs::create_directories(leaf);
    ensureProject(leaf,language,mode,meta);
    auto layout=layoutOf(language,mode);
    auto code=leaf/wide(layout.code);
    fs::create_directories(code.parent_path());
    writeFile(code,source);
    // 目录里已经有代码了，占位用的 .gitkeep 就该让位。
    std::error_code ignored;
    fs::remove(leaf/L".gitkeep",ignored);
    auto relative=code.lexically_relative(executableDirectory());
    return {{"ok",true},{"path",utf8(code.wstring())},{"relative",utf8(relative.wstring())},
            {"problem",utf8((problemDirectory(problemId)).lexically_relative(solveRecordRoot()).wstring())},
            {"language",language},{"mode",mode},{"file",layout.code}};
}

Json listSolveRecords(const std::string& problemId) {
    Json records=Json::array();
    fs::path root;
    try { root=problemId.empty()?solveRecordRoot():problemDirectory(problemId); }
    catch(...) { return {{"root",utf8(solveRecordRoot().wstring())},{"records",records}}; }
    std::error_code error;
    if(!fs::is_directory(root,error)) return {{"root",utf8(solveRecordRoot().wstring())},{"records",records}};
    if(!problemId.empty()) {
        for(const auto& language:{"cpp","cangjie","python","java"})
            for(const auto& mode:{"full","function"}) {
                Json item=leafStatus(root/wide(language)/wide(mode),language,mode);
                item["path"]=utf8((root/wide(language)/wide(mode)).lexically_relative(solveRecordRoot()).wstring());
                records.push_back(item);
            }
    }
    return {{"root",utf8(solveRecordRoot().wstring())},{"problem",problemId.empty()?std::string():utf8(root.lexically_relative(solveRecordRoot()).wstring())},
            {"records",records}};
}

Json scaffoldSolveRecord(const std::string& problemId) {
    auto meta=problemMeta(problemId);
    auto base=problemDirectory(problemId);
    Json created=Json::array();
    for(const auto& language:{"cpp","cangjie","python","java"})
        for(const auto& mode:{"full","function"}) {
            auto leaf=base/wide(language)/wide(mode);
            bool existed=fs::is_directory(leaf);
            fs::create_directories(leaf);
            ensureProject(leaf,std::string(language),std::string(mode),meta);
            created.push_back({{"language",language},{"mode",mode},{"created",!existed}});
        }
    return {{"ok",true},{"problem",utf8(base.lexically_relative(solveRecordRoot()).wstring())},
            {"path",utf8(base.wstring())},{"leaves",created}};
}
