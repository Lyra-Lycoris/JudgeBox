#pragma once
#include "compiler.hpp"
#include "data.hpp"
#include "files.hpp"
#include "problems.hpp"
#include "process.hpp"
#include <mutex>
#include <thread>

// 导入自检（problems.cpp）与正式判题共用同一套编译/运行原语，避免两处语义漂移。
struct CaseJudgement {
    std::string verdict,message;
    double timeMs=0;
    long long memoryBytes=0;
};
std::string assembleCpp(const std::string& driver,const std::vector<std::string>& units);
std::vector<std::pair<std::string,std::string>> assembleCangjie(const std::string& driver,const std::string& package,
                                                                 const std::vector<std::string>& units,bool functionMode);
// 把 driver 与选手源码拼成一份完整程序（完整式提交的参考程序 / 一次性源码）。
// cpp：driver + 源码；python：源码 + driver（driver 自带 import 与入口）；java：平台补 import 与 class Main；
// cangjie：合并 package/import 后拼成一个 .cj 文件。
std::string assembleFullSource(const std::string& language,const std::string& driver,
                               const std::string& source,const std::string& package);
// 函数式提交的编译单元：cpp/python/java 是单文件，cangjie 是 main.cj + solve.cj。
std::vector<std::pair<std::string,std::string>> assembleFunction(const std::string& language,const std::string& driver,
                                                                 const std::string& source,const std::string& package);
Program buildChecker(const std::string& source,const fs::path& directory,const Json& tools,const std::atomic_bool* cancel);
Program buildUnit(const std::string& language,const std::vector<std::pair<std::string,std::string>>& files,
                  const fs::path& directory,const Json& tools,const std::atomic_bool* cancel);
CaseJudgement judgeCase(const Program& program,const fs::path& directory,const CaseFile& test,const Program* checker,
                        long long timeMs,long long memoryMb,const std::atomic_bool* cancel);

Json runCustomTests(const fs::path& cacheRoot,const fs::path& dataDir,const Json& tools,const std::string& problemId,const Json& request);

class ProblemJudgeEngine {
    fs::path cacheRoot,dataDir;
    Json tools,state;
    std::mutex mutex;
    std::atomic_bool cancel{false};
    std::thread worker;
    void execute(Json request,fs::path directory);
    void update(const Json& fields);
public:
    ProblemJudgeEngine(fs::path cacheRoot,fs::path dataDir,Json tools);
    ~ProblemJudgeEngine();
    Json start(const Json& request);
    Json status();
    void stop();
};
