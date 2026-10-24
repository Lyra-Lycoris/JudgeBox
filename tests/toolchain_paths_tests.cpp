#include "compiler.hpp"
#include "path_compat.hpp"
#include <iostream>
#include <stdexcept>
#include <future>
#include <barrier>
void check(bool ok,const char* message){if(!ok)throw std::runtime_error(message);}
int main(){
    auto root=fs::temp_directory_path()/(L"JudgeBox bundled paths "+std::to_wstring(GetTickCount64()));
    try {
        for(const auto& file:{L"gcc/bin/g++.exe",L"python/python.exe",L"jdk/bin/java.exe",L"jdk/bin/javac.exe",L"cangjie/bin/cjc.exe"}) {
            auto p=root/L"runtimes"/file;fs::create_directories(p.parent_path());writeFile(p,"");
        }
        auto bundled=bundledTools(root);
        check(fs::equivalent(fs::path(wide(bundled.at("cpp"))),root/L"runtimes/gcc/bin/g++.exe"),"language service must use the installed GCC");
        check(bundledTools(root/L"not-installed").at("cpp")=="","language service must not use a compiler outside the install");
        writeFile(root/L"runtimes/manifest.json","{}");
        auto tools=detectTools(root);
        check(fs::equivalent(fs::path(wide(tools.at("cpp"))),root/L"runtimes/gcc/bin/g++.exe"),"bundled GCC must win over PATH");
        check(fs::equivalent(fs::path(wide(tools.at("python"))),root/L"runtimes/python/python.exe"),"bundled Python");
        check(fs::equivalent(fs::path(wide(tools.at("java"))),root/L"runtimes/jdk/bin/java.exe"),"bundled JVM");
        fs::remove(root/L"runtimes/gcc/bin/g++.exe");
        check(detectTools(root).at("cpp")=="","damaged bundle must not silently use developer GCC");
        check(bundledTools(root).at("cpp")=="","language service must not replace a missing bundled compiler");
        auto repo=fs::temp_directory_path()/(L"JudgeBox dev runtime "+std::to_wstring(GetTickCount64()));
        auto staged=repo/L".runtime/stage/JudgeBox/runtimes";
        fs::create_directories(staged/L"cangjie/bin");
        fs::create_directories(repo/L"build");
        writeFile(staged/L"cangjie/bin/cjc.exe","");
        writeFile(staged/L"manifest.json","{}");
        auto fromRoot=bundledTools(repo);
        check(fs::equivalent(fs::path(wide(fromRoot.at("cangjie"))),staged/L"cangjie/bin/cjc.exe"),"repo exe must use the staged Cangjie toolchain");
        auto fromBuild=bundledTools(repo/L"build");
        check(fs::equivalent(fs::path(wide(fromBuild.at("cangjie"))),staged/L"cangjie/bin/cjc.exe"),"build exe must use the staged Cangjie toolchain");
        auto detected=detectTools(repo);
        check(detected.at("cpp")=="","staged manifest must keep the dev build on the bundled toolchain");
        check(fs::equivalent(fs::path(wide(detected.at("cangjie"))),staged/L"cangjie/bin/cjc.exe"),"dev detection must keep the staged Cangjie compiler");
        fs::remove_all(repo);
        auto unicodeDirectory=fs::current_path()/(L"JudgeBox 中文 concurrent "+std::to_wstring(GetTickCount64()));
        fs::create_directories(unicodeDirectory);
        std::barrier ready(8);std::vector<std::future<fs::path>> aliases;
        for(int i=0;i<8;++i)aliases.push_back(std::async(std::launch::async,[&]{ready.arrive_and_wait();return asciiDirectory(unicodeDirectory);}));
        writeFile(unicodeDirectory/L"marker.txt","junction-ok");
        for(auto& alias:aliases)check(readFile(alias.get()/L"marker.txt")=="junction-ok","concurrent first-use junction must be valid");
        fs::remove(unicodeDirectory/L"marker.txt");
        fs::remove(unicodeDirectory);
        for(auto i=fs::recursive_directory_iterator(root);i!=fs::recursive_directory_iterator();++i)if(i->is_regular_file())fs::remove(i->path());
        // All targets are inside the unique test-owned directory under TEMP.
        fs::remove_all(root);
        std::cout<<"toolchain path tests passed\n";
    }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}
}
