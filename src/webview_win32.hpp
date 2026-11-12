#pragma once
#include <windows.h>
#include <functional>
#include <string>

// Opens the JudgeBox UI in a native window backed by the installed WebView2 runtime.
// Returns 0 after the window closes, 3 when the WebView2 runtime is unavailable.
int runWebViewWindow(HINSTANCE instance,const std::wstring& url,const std::function<void()>& requestStop);
// Fallback for machines without WebView2: an Edge app window, still without a console.
bool runEdgeAppWindow(const std::wstring& url,const std::function<void()>& requestStop);
void postWindowServerStopped();
