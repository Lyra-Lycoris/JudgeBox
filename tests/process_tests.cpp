#include "process.hpp"
#include <windows.h>
#include <filesystem>
#include <iostream>
#include <stdexcept>
#include <thread>
#include <chrono>
void require(bool value, const char* message) { if (!value) throw std::runtime_error(message); }
int main(int, char** argv) {
    try {
        auto exe=std::filesystem::absolute(argv[1]).wstring();
        auto r=runTask(exe,L"", "hello\n",1000,256*1024*1024);
        require(r.started && r.errorMessage.empty(),"echo starts");
        require(r.stdOut=="hello\n" && r.errOut=="diagnostic","stdin/stdout/stderr round trip");
        r=runTask(exe,L"exit","",1000,256*1024*1024); require(r.exit==7,"exit code");
        r=runTask(exe,L"loop","",80,256*1024*1024); require(r.TLE && r.runTimeMs<2000,"TLE");
        r=runTask(exe,L"dual","",2000,256*1024*1024); require(r.stdOut.size()==524288 && r.errOut.size()==524288 && !r.TLE,"concurrent streams");
        std::string large(1024*1024,'i'); r=runTask(exe,L"",large,2000,256*1024*1024); require(r.stdOut==large,"large input");
        r=runTask(exe,L"memory","",2000,32*1024*1024); require(r.MLE,"real MLE");
        r=runTask(L"Z:\\__missing__.exe",L"","",1000,256*1024*1024); require(!r.started && !r.errorMessage.empty(),"launch failure");
        r=runTask(exe,L"","",1000,256*1024*1024); require(r.stdOut.empty() && r.exit==0 && !r.TLE,"empty input EOF");
        RunOptions opt; opt.outputBytes=8192;
        r=runProcess(exe,{L"flood"},"",opt); require(r.OLE && r.stdOut.size()+r.errOut.size()<=8192,"OLE bounded capture");
        std::atomic_bool cancel{false}; opt.cancel=&cancel; opt.timeMs=5000;
        std::thread stopper([&]{std::this_thread::sleep_for(std::chrono::milliseconds(60)); cancel=true;});
        r=runProcess(exe,{L"loop"},large,opt); stopper.join(); require(r.cancelled && !r.TLE && r.runTimeMs<1000,"cancel with blocked stdin writer");
        r=runTask(exe,L"child","",100,256*1024*1024); require(r.TLE,"child timeout");
        auto pid=static_cast<DWORD>(std::stoul(r.stdOut)); HANDLE child=OpenProcess(SYNCHRONIZE,FALSE,pid);
        if(child) { auto ended=WaitForSingleObject(child,1000); CloseHandle(child); require(ended==WAIT_OBJECT_0,"child process reaped"); }
        auto dir=std::filesystem::temp_directory_path()/(L"JudgeBox 中文 空格 "+std::to_wstring(GetTickCount64()));
        std::filesystem::create_directories(dir); auto unicodeExe=dir/L"运行 程序.exe"; std::filesystem::copy_file(exe,unicodeExe);
        r=runTask(unicodeExe.wstring(),L"","unicode path",1000,256*1024*1024);
        std::filesystem::remove(unicodeExe); std::filesystem::remove(dir);
        require(r.started && r.stdOut=="unicode path","Unicode and spaces executable path");
        require(quoteArgument(L"abc\\")==L"\"abc\\\\\"","trailing backslash quoting");
        r=runTask(exe,L"","",1000,-1); require(!r.started && !r.errorMessage.empty(),"negative memory limit rejected");
        std::cout << "process tests passed\n";
    } catch (const std::exception& e) { std::cerr << e.what() << '\n'; return 1; }
}
