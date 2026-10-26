#pragma once
#include <atomic>
#include <cstdint>
#include <string>
#include <vector>

// Reported time: user-mode job CPU time in milliseconds; limits use wall time. Memory: peak job committed bytes.
struct runResult {
    std::uint32_t exit = 0;
    std::string stdOut, errOut, errorMessage;
    double runTimeMs = 0;
    long long runMemory = 0;
    bool started = false, TLE = false, MLE = false, OLE = false, cancelled = false;
};
struct RunOptions {
    long long timeMs = 1000;
    std::uint64_t memoryBytes = 256ULL * 1024 * 1024;
    std::size_t outputBytes = 1024 * 1024;
    std::wstring workingDirectory;
    const std::atomic_bool* cancel = nullptr;
    std::vector<std::wstring> pathEntries;
    std::vector<std::pair<std::wstring,std::wstring>> environment; // Empty value removes an inherited variable.
};
std::wstring quoteArgument(const std::wstring& arg);
runResult runProcess(const std::wstring& exe, const std::vector<std::wstring>& args,
                     const std::string& input, const RunOptions& options = {});
runResult runTask(const std::wstring& exe, const std::wstring& arguments,
                  const std::string& input, const long long& timeMs, const long long& memoryBytes);
