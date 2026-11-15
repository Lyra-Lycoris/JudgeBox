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
// 题库界面用：直接提交 JSON（元数据 + 测试数据 + 可选代码文件）新建或编辑一道题。
Json saveProblem(const fs::path& dataDir,const Json& request);
// 编辑对话框用：返回原始 problem.json、题包内的代码文件，以及测试数据。
Json packageDetail(const fs::path& dataDir,const std::string& id);
Json problemCases(const fs::path& dataDir,const std::string& id);
// 从本地目录收集成对的 .in / .ans，给「新建题目」直接用。
Json scanCaseDirectory(const std::string& directory);
bool deleteProblem(const fs::path& dataDir,const std::string& id);
ProblemPackage openProblem(const fs::path& dataDir,const std::string& id,const fs::path& workDirectory);
Json problemMeta(const std::string& id);
