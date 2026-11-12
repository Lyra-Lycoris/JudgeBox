#include "server.hpp"
#include "compiler.hpp"
#include "webview_win32.hpp"
#include <shlobj.h>
#include <shellapi.h>
#include <cstdio>
#include <chrono>
#include <iostream>
#include <future>
#include <thread>

namespace {
bool g_console = false;

bool ensureConsole() {
    HANDLE output = GetStdHandle(STD_OUTPUT_HANDLE);
    HANDLE error = GetStdHandle(STD_ERROR_HANDLE);
    const bool hasOutput = output && output != INVALID_HANDLE_VALUE;
    const bool hasError = error && error != INVALID_HANDLE_VALUE;
    if (!hasOutput && !hasError) {
        bool attached = AttachConsole(ATTACH_PARENT_PROCESS) != FALSE;
        if (!attached) attached = AllocConsole() != FALSE;
        if (!attached) return false;
        std::freopen("CONOUT$","w",stdout);
        std::freopen("CONOUT$","w",stderr);
        std::freopen("CONIN$","r",stdin);
    }
    SetConsoleOutputCP(CP_UTF8);
    return true;
}

void reportError(const std::wstring& message,bool console) {
    if (console) {
        try { std::cerr << utf8(message) << std::endl; } catch (...) {}
    } else {
        MessageBoxW(nullptr,message.c_str(),L"JudgeBox",MB_ICONERROR);
    }
}

std::wstring errorText(const std::exception& error) {
    try { return wide(error.what()); }
    catch (...) { return L"JudgeBox 遇到未知错误。"; }
}

int runSelfTest(const fs::path& data) {
    auto tools = detectTools();
    auto script = executableDirectory() / L"diagnostics/toolchain_matrix.py";
    if (tools.at("python") == "" || !fs::is_regular_file(script)) {
        throw std::runtime_error("Offline toolchains and diagnostics are required for --self-test");
    }
    auto report = data / L"toolchain-self-test.json";
    fs::create_directories(data);
    RunOptions opt;
    opt.timeMs = 600000;
    opt.memoryBytes = 4ULL * 1024 * 1024 * 1024;
    opt.outputBytes = 4 * 1024 * 1024;
    opt.workingDirectory = executableDirectory().wstring();
    std::cout << "Testing bundled C++, Python, Java and Cangjie toolchains..." << std::endl;
    auto result = runProcess(wide(tools.at("python")), {L"-X", L"utf8", script.wstring(), (executableDirectory() / L"JudgeBox.exe").wstring(), L"--clean", L"--bundled", L"--report", report.wstring()}, "", opt);
    std::cout << result.stdOut << result.errOut << std::endl;
    if (!result.errorMessage.empty()) {
        std::cerr << result.errorMessage << std::endl;
    }
    std::cout << "Report: " << utf8(report.wstring()) << std::endl;
    return result.started && !result.TLE && !result.MLE && !result.OLE && result.errorMessage.empty() && result.exit == 0 ? 0 : 1;
}

int runWindowMode(HINSTANCE instance,const fs::path& data,unsigned short port) {
    HANDLE instanceMutex = CreateMutexW(nullptr,TRUE,L"Local\\JudgeBox.Window");
    if (instanceMutex && GetLastError() == ERROR_ALREADY_EXISTS) {
        HWND existing = FindWindowW(L"JudgeBoxMainWindow",nullptr);
        if (existing) {
            ShowWindow(existing,SW_RESTORE);
            SetForegroundWindow(existing);
        }
        CloseHandle(instanceMutex);
        return 0;
    }
    std::promise<std::string> ready;
    auto urlFuture = ready.get_future();
    std::thread server([&]() {
        try {
            ServeHooks hooks;
            hooks.quiet = true;
            hooks.ready = [&ready](const std::string& url) {
                try { ready.set_value(url); } catch (...) {}
            };
            hooks.stopped = []() { postWindowServerStopped(); };
            serve(data,false,port,hooks);
        } catch (...) {
            try { ready.set_exception(std::current_exception()); } catch (...) {}
            postWindowServerStopped();
        }
    });
    int result = 1;
    try {
        if (urlFuture.wait_for(std::chrono::seconds(20)) != std::future_status::ready) {
            throw std::runtime_error("本地引擎启动超时，请检查 127.0.0.1 端口是否被占用。");
        }
        std::string url = urlFuture.get();
        result = runWebViewWindow(instance,wide(url),[]() { requestServerStop(); });
        if (result == 3 && runEdgeAppWindow(wide(url),[]() { requestServerStop(); })) result = 0;
        if (result != 0) {
            throw std::runtime_error("JudgeBox 无法创建界面窗口。请安装 Microsoft Edge WebView2 运行库：https://go.microsoft.com/fwlink/p/?LinkId=2124703");
        }
    } catch (...) {
        requestServerStop();
        if (server.joinable()) server.join();
        if (instanceMutex) CloseHandle(instanceMutex);
        throw;
    }
    requestServerStop();
    if (server.joinable()) server.join();
    if (instanceMutex) CloseHandle(instanceMutex);
    return 0;
}

int run(HINSTANCE instance,int argc,wchar_t** argv) {
    PWSTR localAppData = nullptr;
    if (FAILED(SHGetKnownFolderPath(FOLDERID_LocalAppData,KF_FLAG_CREATE,nullptr,&localAppData))) {
        throw std::runtime_error("Cannot locate the current user's data directory");
    }
    fs::path data = fs::path(localAppData) / L"JudgeBox" / L"runs";
    CoTaskMemFree(localAppData);
    bool selfTest = false, windowMode = true, browser = false;
    unsigned short port = 0;
    for (int i = 1; i < argc; ++i) {
        std::wstring arg = argv[i];
        if (arg == L"--no-browser") {
            windowMode = false;
            browser = false;
        } else if (arg == L"--browser" || arg == L"--no-window") {
            windowMode = false;
            browser = true;
        } else if (arg == L"--window") {
            windowMode = true;
        } else if (arg == L"--self-test") {
            selfTest = true;
        } else if (arg == L"--data-dir" && i + 1 < argc) {
            data = fs::absolute(argv[++i]);
        } else if (arg == L"--port" && i + 1 < argc) {
            int n = std::stoi(argv[++i]);
            if (n < 0 || n > 65535) throw std::runtime_error("端口范围 0..65535");
            port = static_cast<unsigned short>(n);
        } else if (arg == L"--help") {
            g_console = ensureConsole() || g_console;
            std::cout << "JudgeBox 1.3.1\n"
                         "Usage: JudgeBox [--window | --browser | --no-browser] [--port 0] [--data-dir PATH]\n"
                         "                [--self-test] [--help]\n"
                         "No option opens the native JudgeBox window. --browser opens the system browser,\n"
                         "--no-browser runs only the local engine and prints its URL (for automation).\n";
            return 0;
        } else if (arg == L"--version") {
            g_console = ensureConsole() || g_console;
            std::cout << "JudgeBox 1.3.1\n";
            return 0;
        } else {
            throw std::runtime_error("未知参数：" + utf8(arg));
        }
    }
    if (selfTest) {
        g_console = ensureConsole() || g_console;
        return runSelfTest(data);
    }
    if (windowMode) {
        return runWindowMode(instance,data,port);
    }
    return serve(data,browser,port);
}
}

int WINAPI wWinMain(HINSTANCE instance,HINSTANCE,PWSTR,int) {
    SetErrorMode(SEM_FAILCRITICALERRORS | SEM_NOGPFAULTERRORBOX);
    int argc = 0;
    LPWSTR* argv = CommandLineToArgvW(GetCommandLineW(),&argc);
    if (!argv) return 1;
    int code = 1;
    try {
        code = run(instance,argc,argv);
    } catch (const std::exception& error) {
        reportError(errorText(error),g_console);
    } catch (...) {
        reportError(L"JudgeBox 遇到未知错误。",g_console);
    }
    LocalFree(argv);
    return code;
}
