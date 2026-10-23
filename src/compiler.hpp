#pragma once
#include "data.hpp"
#include "files.hpp"
#include "process.hpp"
struct Program {
    std::wstring exe;
    std::vector<std::wstring> args;
    fs::path classDirectory;
    bool java=false;
    std::vector<std::wstring> pathEntries;
    std::vector<std::pair<std::wstring,std::wstring>> environment;
    std::string verdict="AC",message,log;
};
Json detectTools(const fs::path& applicationDirectory=executableDirectory());
Program compileProgram(const std::string& source,const std::string& language,const fs::path& directory,
                       const Json& tools,const std::atomic_bool* cancel);
