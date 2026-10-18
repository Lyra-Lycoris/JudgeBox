//声明进程运行结果
#pragma once
#include<string>
#include<cstdint>

struct runResult{
    std::uint32_t exit=0;//仅在成功取得退出码后有效
    std::string stdOut; //标准输出
    std::string errOut; //错误输出
    long long runTimeMs = 0;//运行时间为毫秒
    long long runMemory = 0;//运行内存用字节

    bool TLE = false;
    bool MLE = false;
    std::string errorMessage;//错误信息

    bool started = false;
    
};

runResult runTask(
    const std::wstring &launchPath, //启动路径
    const std::wstring &arguments, //命令行参数
    const std::string &input, //cin 
    const long long &timeLimitMs,
    const long long &memoryLimit
);