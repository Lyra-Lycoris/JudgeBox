#include <windows.h>
#include <iostream>
#include <string>
#include <vector>
#include <fcntl.h>
#include <io.h>
int main(int argc, char** argv) {
    _setmode(_fileno(stdin), _O_BINARY); _setmode(_fileno(stdout), _O_BINARY); _setmode(_fileno(stderr), _O_BINARY);
    SetErrorMode(SEM_FAILCRITICALERRORS | SEM_NOGPFAULTERRORBOX);
    std::string mode = argc > 1 ? argv[1] : "echo";
    if (mode == "exit") return 7;
    if (mode == "sleep") { Sleep(250); return 0; }
    if (mode == "loop") { for (;;) Sleep(10); }
    if (mode == "memory") {
        std::vector<void*> blocks;
        for (;;) { auto p = VirtualAlloc(nullptr, 4*1024*1024, MEM_COMMIT|MEM_RESERVE, PAGE_READWRITE); if (!p) return 9; blocks.push_back(p); memset(p, 1, 4*1024*1024); }
    }
    if (mode == "flood") { for (;;) std::cout << std::string(4096, 'x') << std::flush; }
    if (mode == "dual") { for (int i=0;i<128;++i) { std::cout << std::string(4096,'o'); std::cerr << std::string(4096,'e'); } return 0; }
    if (mode == "child") {
        wchar_t path[32768]; GetModuleFileNameW(nullptr,path,32768);
        std::wstring cmd=L"\""+std::wstring(path)+L"\" loop";
        STARTUPINFOW si{}; si.cb=sizeof(si); PROCESS_INFORMATION pi{};
        if (!CreateProcessW(path,cmd.data(),nullptr,nullptr,FALSE,CREATE_NO_WINDOW,nullptr,nullptr,&si,&pi)) return 8;
        std::cout << pi.dwProcessId << std::endl; CloseHandle(pi.hThread); CloseHandle(pi.hProcess);
        for (;;) Sleep(10);
    }
    std::string s((std::istreambuf_iterator<char>(std::cin)),{});
    std::cout << s; std::cerr << "diagnostic";
}
