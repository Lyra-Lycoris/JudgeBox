#include <windows.h>
#include "process.hpp"
#include <chrono>

runResult runTask(
    const std::wstring &launchPath,
    const std::wstring &arguments,
    const std::string &input,
    const long long &timeLimitMs,
    const long long &memoryLimit)
{

    runResult result{};

    // 先检查时间限制是否合法
    if (timeLimitMs <= 0 || timeLimitMs >= static_cast<long long>(INFINITE))
    {
        result.errorMessage = "TimeLimit is invalid";
        return result;
    }

    STARTUPINFOW startup{};        // 程序启动配置的结构体
    startup.cb = sizeof(startup);  // 定内存大小
    PROCESS_INFORMATION process{}; // 保存进程创建后的返回信息

    // 拼接命令行指令
    std::wstring commandLine = L"\"" + launchPath + L"\""; // 处理路径
    if (!arguments.empty())
    {
        commandLine += L" " + arguments; // 拼接命令行参数
    }

    const auto startTime = std::chrono::steady_clock::now();//用单调时钟，计算经过时间 

    BOOL created = CreateProcessW( // 创建进程
        launchPath.c_str(),        //.exe 的启动路径，.c_str是指向字符串内容的字符指针
        commandLine.data(),        // 命令行的可修改字符缓冲区
        nullptr,                   //
        nullptr,                   // 进程线程的安全属性，采用默认设置
        FALSE,                     // 不启用一般的可继承句柄传递
        0,                         // 默认创建方式
        nullptr,                   // 沿用JudgeBox的环境变量
        nullptr,                   // 沿用↑ 的工作目录
        &startup,                  // 启动柜配置地址交给Windows读取
        &process);                 // 结果存放位置交给Windows填写

    // 创建失败↓
    if (!created)
    {
        const DWORD code = GetLastError(); // 通过无符号32位整数(DWORD)读取错误返回
        result.errorMessage = "CreateProcessW Error: " + std::to_string(code);
        return result;
    }

    result.started = true; // 成功启动

    // 等待进程
    const DWORD waitStatus = WaitForSingleObject(process.hProcess, static_cast<DWORD>(timeLimitMs));
    if (waitStatus == WAIT_FAILED)
    {
        const DWORD code = GetLastError();
        result.errorMessage = "Wait Error: " + std::to_string(code);

        CloseHandle(process.hProcess);
        CloseHandle(process.hThread); // 关掉句柄
        return result;
    }
    
    //能走到这里就没有失败
    //记录运行时间
    const auto endTime = std::chrono::steady_clock::now();
    result.runTimeMs=std::chrono::duration_cast<std::chrono::milliseconds>(endTime-startTime).count();

    if (waitStatus == WAIT_TIMEOUT)
    {
        // 超时分支完善
        result.TLE = true;

        if (!TerminateProcess(process.hProcess, 1))
        { // 强制关闭进程，关闭发起失败走if分支
            const DWORD code = GetLastError();

            if (WaitForSingleObject(process.hProcess, 0) != WAIT_OBJECT_0)
            {
                // 检测线程运行时间，0代表仅检测程序是否已经被清理
                result.errorMessage = "TerminateProcess Error: " + std::to_string(code);
            }
        }
        else // 关闭成功
        {
            const DWORD stopStatus = WaitForSingleObject(process.hProcess, 1145); // 确认是否已经完全结束
            if (stopStatus == WAIT_FAILED)
            {
                //等待结束失败
                const DWORD code = GetLastError();
                result.errorMessage = "Waiting for termination failed: " + std::to_string(code);
            }else if(stopStatus == WAIT_TIMEOUT){
                //超时不是执行失败
                result.errorMessage = "Waiting for termination Didn't Finish in time";
            }
        }

        if (!result.errorMessage.empty())
        {
            CloseHandle(process.hProcess);
            CloseHandle(process.hThread);
            return result;
        }
    }

    // 退出码
    DWORD exitCode = 0;
    if (GetExitCodeProcess(process.hProcess, &exitCode))
    {
        result.exit = exitCode;
    }
    else
    {
        const DWORD code = GetLastError();
        result.errorMessage = "GetExitCodeProcess failed: " + std::to_string(code);
    }

    CloseHandle(process.hProcess);
    CloseHandle(process.hThread);

    return result;
}