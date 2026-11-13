#include "ziputil.hpp"
#include "process.hpp"
#include <algorithm>

namespace {
// bsdtar ships with Windows 10 1803+ and already understands zip, so the project
// needs no third-party archive library.
const fs::path tarExecutable=L"C:\\Windows\\System32\\tar.exe";

runResult runTar(const std::vector<std::wstring>& arguments,const fs::path& workingDirectory) {
    if(!fs::is_regular_file(tarExecutable)) throw std::runtime_error("系统缺少 tar.exe，无法读写 data.zip");
    RunOptions options;
    options.timeMs=120000;
    options.memoryBytes=512ULL*1024*1024;
    options.outputBytes=256*1024;
    options.workingDirectory=workingDirectory.wstring();
    return runProcess(tarExecutable.wstring(),arguments,"",options);
}
void checkTar(const runResult& result,const char* action) {
    if(!result.started || !result.errorMessage.empty())
        throw std::runtime_error(std::string("无法启动 tar.exe（")+action+"）："+result.errorMessage);
    if(result.TLE || result.MLE || result.OLE)
        throw std::runtime_error(std::string("tar.exe ") + action+"超时或超出资源限制");
    if(result.exit) {
        auto detail=result.errOut+result.stdOut;
        if(detail.empty()) detail="退出码 "+std::to_string(result.exit);
        if(detail.size()>2000) detail.resize(2000);
        throw std::runtime_error(std::string("data.zip ") + action+"失败："+detail);
    }
}
}
void extractZip(const fs::path& zip,const fs::path& destination) {
    if(!fs::is_regular_file(zip)) throw std::runtime_error("找不到数据包："+utf8(zip.wstring()));
    fs::create_directories(destination);
    checkTar(runTar({L"-xf",zip.wstring(),L"-C",destination.wstring()},destination),"解压");
    // tar already refuses most escapes, but the archive is untrusted input: verify
    // every entry really landed under the destination and bound the file count.
    std::error_code error;
    auto root=fs::weakly_canonical(destination,error);
    if(error) throw std::runtime_error("无法解析解压目录："+utf8(destination.wstring()));
    std::size_t count=0;
    for(const auto& entry:fs::recursive_directory_iterator(destination,fs::directory_options::skip_permission_denied)) {
        if(!entry.is_regular_file()) continue;
        auto resolved=fs::weakly_canonical(entry.path(),error);
        if(error) throw std::runtime_error("data.zip 含有无法识别的路径："+utf8(entry.path().filename().wstring()));
        auto relative=resolved.lexically_relative(root);
        if(relative.empty() || relative.is_absolute() || *relative.begin()==fs::path(L".."))
            throw std::runtime_error("data.zip 含有越界路径："+utf8(entry.path().wstring()));
        if(++count>500) throw std::runtime_error("data.zip 文件数超过 500");
    }
}
void createZip(const fs::path& zip,const fs::path& sourceDirectory) {
    if(!fs::is_directory(sourceDirectory)) throw std::runtime_error("打包目录不存在："+utf8(sourceDirectory.wstring()));
    auto parent=zip.parent_path();
    if(!parent.empty()) fs::create_directories(parent);
    std::error_code error; fs::remove(zip,error);
    checkTar(runTar({L"-a",L"-cf",zip.wstring(),L"-C",sourceDirectory.wstring(),L"."},sourceDirectory),"打包");
    if(!fs::is_regular_file(zip)) throw std::runtime_error("data.zip 打包后不存在");
}
