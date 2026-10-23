#pragma once
#include "compiler.hpp"
#include <mutex>
#include <thread>
class JudgeEngine {
    fs::path root,current;
    Json defaultTools,state;
    std::mutex mutex;
    std::atomic_bool cancel{false};
    std::thread worker;
    void execute(Json request,fs::path directory);
    void update(const Json& fields);
public:
    JudgeEngine(fs::path root,Json tools);
    ~JudgeEngine();
    Json status();
    Json start(const Json& request);
    void stop();
    Json detail(int index);
    Json preview(const Json& request);
};
