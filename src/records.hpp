#pragma once
#include "data.hpp"
#include "files.hpp"

// 做题记录：exe 同级的 solveRecord/<专题>/<题目>/<语言>/<提交方式>/ 下保存选手自己的代码。
// 仓颉与 Java 的每个叶子目录都是一个能单独打开的小工程（cjpm.toml / pom.xml）。
fs::path solveRecordRoot();
Json saveSolveRecord(const std::string& problemId,const std::string& language,const std::string& mode,const std::string& source);
Json listSolveRecords(const std::string& problemId);
// 为一道题把八个叶子目录（4 语言 × 2 方式）连同工程骨架一次建好；已存在的文件不覆盖。
Json scaffoldSolveRecord(const std::string& problemId);
