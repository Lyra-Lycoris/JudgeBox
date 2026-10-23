#include "server.hpp"
#include "compiler.hpp"
#include <shlobj.h>
#include <iostream>
int wmain(int argc,wchar_t** argv) {
    SetConsoleOutputCP(CP_UTF8);
    SetErrorMode(SEM_FAILCRITICALERRORS|SEM_NOGPFAULTERRORBOX);
    try {
        PWSTR localAppData=nullptr;
        if(FAILED(SHGetKnownFolderPath(FOLDERID_LocalAppData,KF_FLAG_CREATE,nullptr,&localAppData))) throw std::runtime_error("Cannot locate the current user's data directory");
        fs::path data=fs::path(localAppData)/L"JudgeBox"/L"runs";
        CoTaskMemFree(localAppData);
        bool browser=true,selfTest=false; unsigned short port=0;
        for(int i=1;i<argc;++i) {
            std::wstring arg=argv[i];
            if(arg==L"--no-browser") browser=false;
            else if(arg==L"--self-test") selfTest=true;
            else if(arg==L"--data-dir" && i+1<argc) data=fs::absolute(argv[++i]);
            else if(arg==L"--port" && i+1<argc) { int n=std::stoi(argv[++i]); if(n<0 || n>65535) throw std::runtime_error("端口范围 0..65535"); port=static_cast<unsigned short>(n); }
            else if(arg==L"--help") { std::cout<<"JudgeBox [--no-browser] [--port 0] [--data-dir PATH] [--self-test]\n"; return 0; }
            else throw std::runtime_error("未知参数："+utf8(arg));
        }
        if(selfTest) {
            auto tools=detectTools(); auto script=executableDirectory()/L"diagnostics/toolchain_matrix.py";
            if(tools.at("python")=="" || !fs::is_regular_file(script)) throw std::runtime_error("Offline toolchains and diagnostics are required for --self-test");
            auto report=data/L"toolchain-self-test.json"; fs::create_directories(data);
            RunOptions opt; opt.timeMs=600000; opt.memoryBytes=4ULL*1024*1024*1024; opt.outputBytes=4*1024*1024; opt.workingDirectory=executableDirectory().wstring();
            std::cout<<"Testing bundled C++, Python, Java and Cangjie toolchains..."<<std::endl;
            auto result=runProcess(wide(tools.at("python")),{L"-X",L"utf8",script.wstring(),(executableDirectory()/L"JudgeBox.exe").wstring(),L"--clean",L"--bundled",L"--report",report.wstring()},"",opt);
            std::cout<<result.stdOut<<result.errOut<<std::endl;
            if(!result.errorMessage.empty()) std::cerr<<result.errorMessage<<std::endl;
            std::cout<<"Report: "<<utf8(report.wstring())<<std::endl;
            return result.started && !result.TLE && !result.MLE && !result.OLE && result.errorMessage.empty() && result.exit==0?0:1;
        }
        return serve(data,browser,port);
    } catch(const std::exception& e) { std::cerr<<"JudgeBox: "<<e.what()<<'\n'; return 1; }
}
