#include "webview_win32.hpp"
#include "files.hpp"
#if defined(__GNUC__)
#pragma GCC diagnostic ignored "-Wunknown-pragmas"
#pragma GCC diagnostic ignored "-Wcast-function-type"
#endif
#include "WebView2.h"
#include <shlobj.h>
#include <shobjidl.h>
#include <shellapi.h>
#include <winreg.h>
#include <algorithm>
#include <cstdio>
#include <vector>

namespace {
constexpr UINT kServerStoppedMessage = WM_APP + 1;
constexpr UINT kWebViewFailedMessage = WM_APP + 2;
constexpr int kWebViewUnavailable = 3;

HWND g_window = nullptr;
ICoreWebView2Controller* g_controller = nullptr;
ICoreWebView2* g_webview = nullptr;
std::function<void()> g_requestStop;
std::wstring g_targetUrl;
HMODULE g_loader = nullptr;
bool g_serverStopped = false;

using CreateEnvironmentFn = HRESULT (STDAPICALLTYPE*)(PCWSTR,PCWSTR,ICoreWebView2EnvironmentOptions*,ICoreWebView2CreateCoreWebView2EnvironmentCompletedHandler*);
using RuntimeVersionFn = HRESULT (STDAPICALLTYPE*)(PCWSTR,LPWSTR*);
CreateEnvironmentFn g_createEnvironment = nullptr;
RuntimeVersionFn g_runtimeVersion = nullptr;

template <typename TInterface>
struct ComHandler : TInterface {
    ULONG refs = 1;
    REFIID identity;
    explicit ComHandler(REFIID iid) : identity(iid) {}
    virtual ~ComHandler() = default;
    HRESULT STDMETHODCALLTYPE QueryInterface(REFIID riid,void** value) override {
        if (!value) return E_POINTER;
        if (IsEqualIID(riid,IID_IUnknown) || IsEqualIID(riid,identity)) {
            *value = static_cast<TInterface*>(this);
            AddRef();
            return S_OK;
        }
        *value = nullptr;
        return E_NOINTERFACE;
    }
    ULONG STDMETHODCALLTYPE AddRef() override { return ++refs; }
    ULONG STDMETHODCALLTYPE Release() override { ULONG n = --refs; if (!n) delete this; return n; }
};

struct EnvironmentHandler final : ComHandler<ICoreWebView2CreateCoreWebView2EnvironmentCompletedHandler> {
    HWND window;
    explicit EnvironmentHandler(HWND hwnd) : ComHandler(IID_ICoreWebView2CreateCoreWebView2EnvironmentCompletedHandler),window(hwnd) {}
    HRESULT STDMETHODCALLTYPE Invoke(HRESULT error,ICoreWebView2Environment* environment) override;
};

struct ControllerHandler final : ComHandler<ICoreWebView2CreateCoreWebView2ControllerCompletedHandler> {
    HWND window;
    explicit ControllerHandler(HWND hwnd) : ComHandler(IID_ICoreWebView2CreateCoreWebView2ControllerCompletedHandler),window(hwnd) {}
    HRESULT STDMETHODCALLTYPE Invoke(HRESULT error,ICoreWebView2Controller* controller) override;
};

struct WindowCloseHandler final : ComHandler<ICoreWebView2WindowCloseRequestedEventHandler> {
    HWND window;
    explicit WindowCloseHandler(HWND hwnd) : ComHandler(IID_ICoreWebView2WindowCloseRequestedEventHandler),window(hwnd) {}
    HRESULT STDMETHODCALLTYPE Invoke(ICoreWebView2*,IUnknown*) override {
        if (IsWindow(window)) PostMessageW(window,WM_CLOSE,0,0);
        return S_OK;
    }
};

struct NewWindowHandler final : ComHandler<ICoreWebView2NewWindowRequestedEventHandler> {
    explicit NewWindowHandler() : ComHandler(IID_ICoreWebView2NewWindowRequestedEventHandler) {}
    HRESULT STDMETHODCALLTYPE Invoke(ICoreWebView2*,ICoreWebView2NewWindowRequestedEventArgs* args) override {
        LPWSTR uri = nullptr;
        if (args && SUCCEEDED(args->get_Uri(&uri)) && uri) {
            ShellExecuteW(nullptr,L"open",uri,nullptr,nullptr,SW_SHOWNORMAL);
            CoTaskMemFree(uri);
        }
        if (args) args->put_Handled(TRUE);
        return S_OK;
    }
};

std::wstring userDataDirectory() {
    PWSTR local = nullptr;
    if (SUCCEEDED(SHGetKnownFolderPath(FOLDERID_LocalAppData,KF_FLAG_CREATE,nullptr,&local))) {
        fs::path path = fs::path(local) / L"JudgeBox" / L"WebView2";
        CoTaskMemFree(local);
        std::error_code error;
        fs::create_directories(path,error);
        if (!error) return path.wstring();
    }
    wchar_t temporary[MAX_PATH]{};
    if (GetTempPathW(MAX_PATH,temporary)) {
        fs::path path = fs::path(temporary) / L"JudgeBox-WebView2";
        std::error_code error;
        fs::create_directories(path,error);
        if (!error) return path.wstring();
    }
    return {};
}

bool loadWebView2() {
    if (g_loader) return true;
    std::error_code error;
    auto local = executableDirectory() / L"WebView2Loader.dll";
    if (fs::is_regular_file(local,error)) g_loader = LoadLibraryW(local.c_str());
    if (!g_loader) return false;
    g_createEnvironment = reinterpret_cast<CreateEnvironmentFn>(GetProcAddress(g_loader,"CreateCoreWebView2EnvironmentWithOptions"));
    g_runtimeVersion = reinterpret_cast<RuntimeVersionFn>(GetProcAddress(g_loader,"GetAvailableCoreWebView2BrowserVersionString"));
    return g_createEnvironment && g_runtimeVersion;
}

bool runtimeInstalled() {
    if (!loadWebView2()) return false;
    LPWSTR version = nullptr;
    HRESULT result = g_runtimeVersion(nullptr,&version);
    const bool found = SUCCEEDED(result) && version != nullptr;
    if (version) CoTaskMemFree(version);
    return found;
}

void closeWebView() {
    if (g_controller) {
        g_controller->Close();
        g_controller->Release();
        g_controller = nullptr;
    }
    if (g_webview) {
        g_webview->Release();
        g_webview = nullptr;
    }
}

void resizeWebView(HWND hwnd) {
    if (!g_controller) return;
    RECT bounds{};
    GetClientRect(hwnd,&bounds);
    g_controller->put_Bounds(bounds);
}

void initializeWebView(HWND hwnd) {
    auto handler = new EnvironmentHandler(hwnd);
    HRESULT result = g_createEnvironment(nullptr,userDataDirectory().c_str(),nullptr,handler);
    handler->Release();
    if (FAILED(result)) {
        PostMessageW(hwnd,kWebViewFailedMessage,static_cast<WPARAM>(result),0);
    }
}

HRESULT STDMETHODCALLTYPE EnvironmentHandler::Invoke(HRESULT error,ICoreWebView2Environment* environment) {
    if (FAILED(error) || !environment) {
        PostMessageW(window,kWebViewFailedMessage,static_cast<WPARAM>(error),0);
        return S_OK;
    }
    auto handler = new ControllerHandler(window);
    HRESULT result = environment->CreateCoreWebView2Controller(window,handler);
    handler->Release();
    if (FAILED(result)) PostMessageW(window,kWebViewFailedMessage,static_cast<WPARAM>(result),0);
    return S_OK;
}

HRESULT STDMETHODCALLTYPE ControllerHandler::Invoke(HRESULT error,ICoreWebView2Controller* controller) {
    if (FAILED(error) || !controller) {
        PostMessageW(window,kWebViewFailedMessage,static_cast<WPARAM>(error),0);
        return S_OK;
    }
    g_controller = controller;
    g_controller->AddRef();
    resizeWebView(window);
    g_controller->put_IsVisible(TRUE);
    if (FAILED(g_controller->get_CoreWebView2(&g_webview)) || !g_webview) {
        PostMessageW(window,kWebViewFailedMessage,static_cast<WPARAM>(E_FAIL),0);
        return S_OK;
    }
    ICoreWebView2Settings* settings = nullptr;
    if (SUCCEEDED(g_webview->get_Settings(&settings)) && settings) {
        settings->put_AreDefaultContextMenusEnabled(FALSE);
        settings->put_AreDevToolsEnabled(FALSE);
        settings->put_IsStatusBarEnabled(FALSE);
        settings->put_IsZoomControlEnabled(FALSE);
        settings->Release();
    }
    EventRegistrationToken token{};
    auto closeHandler = new WindowCloseHandler(window);
    g_webview->add_WindowCloseRequested(closeHandler,&token);
    closeHandler->Release();
    auto newWindowHandler = new NewWindowHandler();
    g_webview->add_NewWindowRequested(newWindowHandler,&token);
    newWindowHandler->Release();
    g_webview->Navigate(g_targetUrl.c_str());
    return S_OK;
}

LRESULT CALLBACK windowProcedure(HWND hwnd,UINT message,WPARAM wParam,LPARAM lParam) {
    switch (message) {
    case WM_CREATE:
        g_window = hwnd;
        if (g_requestStop) initializeWebView(hwnd);
        return 0;
    case WM_SIZE:
        resizeWebView(hwnd);
        return 0;
    case WM_SETFOCUS:
        if (g_controller) g_controller->MoveFocus(COREWEBVIEW2_MOVE_FOCUS_REASON_PROGRAMMATIC);
        return 0;
    case WM_GETMINMAXINFO: {
        auto info = reinterpret_cast<MINMAXINFO*>(lParam);
        info->ptMinTrackSize.x = 900;
        info->ptMinTrackSize.y = 600;
        return 0;
    }
    case WM_DPICHANGED: {
        auto suggested = reinterpret_cast<RECT*>(lParam);
        SetWindowPos(hwnd,nullptr,suggested->left,suggested->top,suggested->right - suggested->left,suggested->bottom - suggested->top,SWP_NOZORDER | SWP_NOACTIVATE);
        resizeWebView(hwnd);
        return 0;
    }
    case WM_CLOSE:
        if (!g_serverStopped && g_requestStop) g_requestStop();
        closeWebView();
        DestroyWindow(hwnd);
        return 0;
    case kServerStoppedMessage:
        if (g_serverStopped) return 0;
        g_serverStopped = true;
        closeWebView();
        DestroyWindow(hwnd);
        return 0;
    case kWebViewFailedMessage: {
        closeWebView();
        std::wstring detail = L"JudgeBox 无法初始化内置浏览器窗口。\n\n错误代码：0x";
        wchar_t code[16]{};
        swprintf(code,16,L"%08X",static_cast<unsigned int>(wParam));
        detail += code;
        MessageBoxW(hwnd,detail.c_str(),L"JudgeBox",MB_ICONERROR);
        DestroyWindow(hwnd);
        return 0;
    }
    case WM_DESTROY:
        g_window = nullptr;
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProcW(hwnd,message,wParam,lParam);
}

std::wstring findEdge() {
    const wchar_t* environmentNames[] = {L"ProgramFiles(x86)",L"ProgramFiles",L"LocalAppData"};
    for (const auto* name : environmentNames) {
        wchar_t root[MAX_PATH]{};
        DWORD length = GetEnvironmentVariableW(name,root,MAX_PATH);
        if (!length || length >= MAX_PATH) continue;
        auto candidate = fs::path(root) / L"Microsoft" / L"Edge" / L"Application" / L"msedge.exe";
        std::error_code error;
        if (fs::is_regular_file(candidate,error)) return candidate.wstring();
    }
    wchar_t value[MAX_PATH]{};
    DWORD size = sizeof(value);
    if (RegGetValueW(HKEY_LOCAL_MACHINE,L"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\msedge.exe",nullptr,RRF_RT_REG_SZ,nullptr,value,&size) == ERROR_SUCCESS) {
        std::error_code error;
        if (fs::is_regular_file(value,error)) return value;
    }
    return {};
}
}

int runWebViewWindow(HINSTANCE instance,const std::wstring& url,const std::function<void()>& requestStop) {
    SetCurrentProcessExplicitAppUserModelID(L"JudgeBox.JudgeBox");
    if (!runtimeInstalled()) return kWebViewUnavailable;
    g_requestStop = requestStop;
    g_targetUrl = url;
    g_serverStopped = false;
    CoInitializeEx(nullptr,COINIT_APARTMENTTHREADED);
    WNDCLASSEXW windowClass{};
    windowClass.cbSize = sizeof(windowClass);
    windowClass.lpfnWndProc = windowProcedure;
    windowClass.hInstance = instance;
    windowClass.hCursor = LoadCursorW(nullptr,IDC_ARROW);
    windowClass.hIcon = static_cast<HICON>(LoadImageW(instance,MAKEINTRESOURCEW(101),IMAGE_ICON,0,0,LR_DEFAULTSIZE | LR_SHARED));
    windowClass.hIconSm = static_cast<HICON>(LoadImageW(instance,MAKEINTRESOURCEW(101),IMAGE_ICON,16,16,LR_SHARED));
    windowClass.hbrBackground = reinterpret_cast<HBRUSH>(COLOR_WINDOW + 1);
    windowClass.lpszClassName = L"JudgeBoxMainWindow";
    if (!RegisterClassExW(&windowClass)) return 1;
    RECT work{};
    SystemParametersInfoW(SPI_GETWORKAREA,0,&work,0);
    int width = 1280,height = 860;
    if (work.right - work.left > 0) width = std::min(width,static_cast<int>(work.right - work.left) - 80);
    if (work.bottom - work.top > 0) height = std::min(height,static_cast<int>(work.bottom - work.top) - 80);
    width = std::max(width,900);
    height = std::max(height,600);
    int x = work.left + ((work.right - work.left) - width) / 2;
    int y = work.top + ((work.bottom - work.top) - height) / 2;
    HWND hwnd = CreateWindowExW(0,windowClass.lpszClassName,L"JudgeBox",WS_OVERLAPPEDWINDOW,x,y,width,height,nullptr,nullptr,instance,nullptr);
    if (!hwnd) return 1;
    ShowWindow(hwnd,SW_SHOW);
    UpdateWindow(hwnd);
    MSG message{};
    while (GetMessageW(&message,nullptr,0,0) > 0) {
        TranslateMessage(&message);
        DispatchMessageW(&message);
    }
    closeWebView();
    g_requestStop = nullptr;
    CoUninitialize();
    return 0;
}

bool runEdgeAppWindow(const std::wstring& url,const std::function<void()>& requestStop) {
    std::wstring edge = findEdge();
    if (edge.empty()) return false;
    std::wstring profile = userDataDirectory() + L"-Edge";
    std::error_code error;
    fs::create_directories(profile,error);
    std::wstring command = L"\"" + edge + L"\" --app=\"" + url + L"\" --user-data-dir=\"" + profile +
        L"\" --no-first-run --no-default-browser-check --disable-background-mode --window-size=1280,860";
    STARTUPINFOW startup{};
    startup.cb = sizeof(startup);
    PROCESS_INFORMATION process{};
    std::vector<wchar_t> mutableCommand(command.begin(),command.end());
    mutableCommand.push_back(L'\0');
    if (!CreateProcessW(nullptr,mutableCommand.data(),nullptr,nullptr,FALSE,CREATE_UNICODE_ENVIRONMENT,nullptr,nullptr,&startup,&process)) return false;
    CloseHandle(process.hThread);
    WaitForSingleObject(process.hProcess,INFINITE);
    CloseHandle(process.hProcess);
    requestStop();
    return true;
}

void postWindowServerStopped() {
    if (g_window) PostMessageW(g_window,kServerStoppedMessage,0,0);
}
