#pragma once
#include <windows.h>
#include <filesystem>
#include <fstream>
#include <string>
#include <stdexcept>
namespace fs = std::filesystem;
inline fs::path executableDirectory() {
    wchar_t path[32768]; DWORD n=GetModuleFileNameW(nullptr,path,32768);
    if(!n || n>=32768) throw std::runtime_error("Cannot locate JudgeBox executable");
    return fs::path(path).parent_path();
}
inline std::wstring wide(const std::string& s) {
    if(s.empty()) return {};
    int n=MultiByteToWideChar(CP_UTF8,MB_ERR_INVALID_CHARS,s.data(),static_cast<int>(s.size()),nullptr,0);
    if(!n) throw std::runtime_error("无效 UTF-8 文本");
    std::wstring w(n,L' '); MultiByteToWideChar(CP_UTF8,MB_ERR_INVALID_CHARS,s.data(),static_cast<int>(s.size()),w.data(),n); return w;
}
inline std::string utf8(const std::wstring& w) {
    if(w.empty()) return {};
    int n=WideCharToMultiByte(CP_UTF8,0,w.data(),static_cast<int>(w.size()),nullptr,0,nullptr,nullptr);
    std::string s(n,' '); WideCharToMultiByte(CP_UTF8,0,w.data(),static_cast<int>(w.size()),s.data(),n,nullptr,nullptr); return s;
}
inline void writeFile(const fs::path& path,const std::string& content) {
    std::ofstream f(path,std::ios::binary); if(!f || !f.write(content.data(),content.size())) throw std::runtime_error("无法写入文件："+utf8(path.wstring()));
}
inline std::string readFile(const fs::path& path) {
    std::ifstream f(path,std::ios::binary); if(!f) throw std::runtime_error("无法读取文件："+utf8(path.wstring()));
    return {std::istreambuf_iterator<char>(f),{}};
}
