#pragma once
#include "data.hpp"
#include "files.hpp"

// 启动后在后台把 GitHub 上的题库增量同步到本地 ProblemDatabase：
// 只拉新增/变化过的题包，界面不等它，同步完前端再刷新题单。
struct SyncSettings {
    bool enabled=true;
    std::string kind="github";    // github | gitee
    std::string repo="Lyra-Lycoris/JudgeBox-ProblemDatabase";
    std::string path="";          // 仓库根目录就是题库目录；留空表示根
    std::string ref="main";
    std::string api="https://api.github.com";
    std::vector<SyncSettings> sources;   // 为空表示只用上面这一个
};

SyncSettings syncSettings();
void startProblemSync();   // 只启动一次；已有同步在跑时直接返回
Json syncStatus();         // 给前端轮询：running / added / updated / total / error / enabled
