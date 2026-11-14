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
