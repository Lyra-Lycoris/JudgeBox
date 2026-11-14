#pragma once
#include "data.hpp"
#include "files.hpp"

// 题包契约见规格 §4：problem.json 只做规范化与校验，用例真正落在 data.zip 里。
struct ProblemCase {
    std::string id,group,input,answer;
};
struct CaseFile {
    std::string id,group;
    fs::path input,answer;
    std::uintmax_t answerBytes=0;
};
struct ProblemPackage {
    Json meta;
    fs::path directory;
    std::vector<CaseFile> cases; // 按 groups 顺序展开
};

fs::path problemDatabase();
fs::path problemsRoot(const fs::path& dataDir);
Json listProblems(const fs::path& dataDir);
Json loadProblem(const fs::path& dataDir,const std::string& id);
Json importProblem(const fs::path& dataDir,const Json& request);
bool deleteProblem(const fs::path& dataDir,const std::string& id);
ProblemPackage openProblem(const fs::path& dataDir,const std::string& id,const fs::path& workDirectory);
Json problemMeta(const std::string& id);
