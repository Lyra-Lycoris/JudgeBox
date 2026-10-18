#include <windows.h>
#include "process.hpp"

runResult runTask(
    const std::wstring &launchPath,
    const std::wstring &arguments,
    const std::string &input,
    const long long &timeLimitMs,
    const long long &memoryLimit)
{

    runResult result{};

    STARTUPINFOW startup{};        // 程序启动配置的结构体
    startup.cb = sizeof(startup);  // 定内存大小
    PROCESS_INFORMATION process{}; // 保存进程创建后的返回信息

    //拼接命令行指令
    std::wstring commandLine = L"\""+launchPath+L"\"";//处理路径
    if(!arguments.empty()){
        commandLine += L" "+arguments;//拼接命令行参数
    }

    BOOL created = CreateProcessW(//创建进程
        launchPath.c_str(),//.exe 的启动路径，.c_str是指向字符串内容的字符指针
        commandLine.data(),    //命令行的可修改字符缓冲区
        nullptr,    //
        nullptr,    //进程线程的安全属性，采用默认设置
        FALSE,      //不启用一般的可继承句柄传递
        0,          //默认创建方式
        nullptr,    //沿用JudgeBox的环境变量
        nullptr,    //沿用↑ 的工作目录
        &startup,   //启动柜配置地址交给Windows读取
        &process);  //结果存放位置交给Windows填写

    //创建失败↓
    if(!created){
        const DWORD code = GetLastError();//通过无符号32位整数(DWORD)读取错误返回
        result.errorMessage = "CreateProcessW Error: "+std::to_string(code);
        return result;
    }

    result.started=true;//成功启动

    //补齐等待，退出码和资源释放
    

    return result;
}