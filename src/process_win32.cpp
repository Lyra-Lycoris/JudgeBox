#include <windows.h>
#include "process.hpp"
#include <chrono>

//创建输出管道函数
static bool createOutPutPipe(HANDLE &readEnd,HANDLE &writeEnd,std::string &errorMessage){
    //允许子程序继承管道句柄
    SECURITY_ATTRIBUTES security{};//安全权限与继承规则结构体
    security.nLength = sizeof(security);//结构体大小，单位是字节
    security.bInheritHandle = TRUE;//允许子程序继承新建的管道句柄

    if(!CreatePipe(&readEnd,&writeEnd,&security,0)){
        const DWORD code=GetLastError();
        errorMessage = "CreatePipe Error: "+std::to_string(code);
        readEnd = nullptr;
        writeEnd = nullptr;
        return false;
    }

    //单独修改读端句柄，使其不被继承
    if (!SetHandleInformation(readEnd, HANDLE_FLAG_INHERIT, 0))
    {
        const DWORD code = GetLastError();
        errorMessage = "SetHandleInformation failed: " + std::to_string(code);
        CloseHandle(readEnd);
        CloseHandle(writeEnd);
        readEnd = nullptr;
        writeEnd = nullptr;
        return false;
    }

    return true;

}

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

    // 标准输出管道：子程序写入，JudgeBox 读取
    HANDLE outRead = nullptr;  // JudgeBox 读取 stdout 的入口
    HANDLE outWrite = nullptr; // 准备交给子程序，用来写入 stdout

    // 标准错误管道：子程序写入，JudgeBox 读取
    HANDLE errRead = nullptr;  // JudgeBox 读取 stderr 的入口
    HANDLE errWrite = nullptr; // 准备交给子程序，用来写入 stderr

    // 统一释放 JudgeBox 持有的管道句柄，避免提前返回时遗漏
    auto closeOutputPipes = [&]() {
        if (outRead != nullptr) {
            CloseHandle(outRead);
            outRead = nullptr;
        }
        if (outWrite != nullptr) {
            CloseHandle(outWrite);
            outWrite = nullptr;
        }
        if (errRead != nullptr) {
            CloseHandle(errRead);
            errRead = nullptr;
        }
        if (errWrite != nullptr) {
            CloseHandle(errWrite);
            errWrite = nullptr;
        }
    };

    // 每次调用创建一条管道，并填入对应的读端、写端句柄
    if (!createOutPutPipe(outRead, outWrite, result.errorMessage)) {
        closeOutputPipes();
        return result;
    }

    if (!createOutPutPipe(errRead, errWrite, result.errorMessage)) {
        closeOutputPipes();
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
        closeOutputPipes();
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
        closeOutputPipes();
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
            closeOutputPipes();
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
    closeOutputPipes();

    return result;
}