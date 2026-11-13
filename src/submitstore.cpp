#include "submitstore.hpp"
#include "apierror.hpp"
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <random>

namespace {
constexpr std::size_t maxPerProblem=50;
constexpr std::size_t maxListed=200;

std::string timestamp(bool withMinutes) {
    SYSTEMTIME now; GetSystemTime(&now);
    char buffer[64];
    if(withMinutes) std::snprintf(buffer,sizeof(buffer),"%04d%02d%02d-%02d%02d%02d",now.wYear,now.wMonth,now.wDay,now.wHour,now.wMinute,now.wSecond);
    else std::snprintf(buffer,sizeof(buffer),"%04d-%02d-%02dT%02d:%02d:%02dZ",now.wYear,now.wMonth,now.wDay,now.wHour,now.wMinute,now.wSecond);
    return buffer;
}
bool isSubmissionName(const std::string& name) {
    auto path=fs::path(wide(name));
    return path.extension()==L".json" && name!="index.json";
}
// Path segments derived from user input must never escape the cache tree.
bool safeSegment(const std::string& text,bool allowDash) {
    if(text.empty() || text.size()>64) return false;
    for(char c:text) {
        bool ok=(c>='a' && c<='z') || (c>='0' && c<='9') || (allowDash && c=='-');
        if(!ok) return false;
    }
    return true;
}
void warn(const std::string& message) { std::fprintf(stderr,"JudgeBox: %s\n",message.c_str()); }

std::vector<Json> loadDirectory(const fs::path& directory) {
    std::vector<Json> items;
    std::error_code error;
    if(!fs::is_directory(directory,error)) return items;
    for(const auto& entry:fs::directory_iterator(directory,error)) {
        if(!entry.is_regular_file()) continue;
        auto name=utf8(entry.path().filename().wstring());
        if(!isSubmissionName(name)) continue;
        try { auto item=Json::parse(readFile(entry.path())); items.push_back(std::move(item)); }
        catch(const std::exception& e) { warn("忽略损坏的提交记录 "+name+"："+e.what()); }
    }
    std::sort(items.begin(),items.end(),[](const Json& a,const Json& b){
        return a.value("id",std::string())>b.value("id",std::string());
    });
    return items;
}
std::vector<fs::path> problemDirectories(const fs::path& root) {
    std::vector<fs::path> directories;
    std::error_code error;
    if(!fs::is_directory(root,error)) return directories;
    for(const auto& entry:fs::directory_iterator(root,error))
        if(entry.is_directory()) directories.push_back(entry.path());
    return directories;
}
std::vector<Json> loadProblem(const fs::path& root,const std::string& problemId) {
    if(!safeSegment(problemId,true)) return {};
    return loadDirectory(root/wide(problemId));
}
Json statOf(const std::vector<Json>& items) {
    Json best=nullptr,lastVerdict=nullptr,lastAt=nullptr;
    long long top=-1;
    for(const auto& item:items) {
        auto score=item.value("score",0LL);
        if(score>top) { top=score; best=score; }
    }
    if(!items.empty()) {
        lastVerdict=items.front().value("verdict",std::string());
        lastAt=items.front().value("at",std::string());
    }
    return {{"bestScore",best},{"attempts",static_cast<long long>(items.size())},
            {"lastVerdict",lastVerdict},{"lastSubmittedAt",lastAt}};
}
void rebuildIndex(const fs::path& directory,const std::vector<Json>& items) {
    Json index=Json::array();
    for(const auto& item:items) index.push_back(submissionSummary(item));
    try { writeFile(directory/L"index.json",index.dump(2)); }
    catch(const std::exception& e) { warn("无法写入提交索引："+std::string(e.what())); }
}
}
fs::path submissionsRoot(const fs::path& cacheRoot) { return cacheRoot/L".cache"/L"submissions"; }
std::string newSubmissionId() {
    static std::mt19937_64 engine([]{
        std::random_device device;
        auto seed=static_cast<std::uint64_t>(std::chrono::high_resolution_clock::now().time_since_epoch().count());
        return seed^(static_cast<std::uint64_t>(device())<<32)^device();
    }());
    char suffix[16];
    std::snprintf(suffix,sizeof(suffix),"%06llx",static_cast<unsigned long long>(engine()&0xFFFFFF));
    return timestamp(true)+"-"+suffix;
}
Json submissionSummary(const Json& submission) {
    auto cases=submission.contains("cases") && submission.at("cases").is_array()?submission.at("cases").size():0;
    long long passed=0;
    if(submission.contains("cases") && submission.at("cases").is_array())
        for(const auto& item:submission.at("cases"))
            if(item.value("verdict",std::string())=="AC") ++passed;
    auto source=submission.value("source",std::string());
    return {{"id",submission.value("id",std::string())},
            {"language",submission.value("language",std::string())},
            {"verdict",submission.value("verdict",std::string())},
            {"score",submission.value("score",0LL)},
            {"cases",static_cast<long long>(cases)},
            {"passed",passed},
            {"at",submission.value("at",std::string())},
            {"sourceBytes",static_cast<long long>(source.size())}};
}
void saveSubmission(const fs::path& cacheRoot,const Json& submission) {
    auto problemId=submission.value("problemId",std::string());
    if(!safeSegment(problemId,true)) throw std::runtime_error("提交记录缺少合法的 problemId");
    auto directory=submissionsRoot(cacheRoot)/wide(problemId);
    fs::create_directories(directory);
    writeFile(directory/(submission.value("id",std::string())+".json"),submission.dump(2));
    auto items=loadDirectory(directory);
    if(items.size()>maxPerProblem) {
        for(std::size_t i=maxPerProblem;i<items.size();++i) {
            std::error_code error;
            fs::remove(directory/(items[i].value("id",std::string())+".json"),error);
        }
        items.resize(maxPerProblem);
    }
    rebuildIndex(directory,items);
}
Json listSubmissions(const fs::path& cacheRoot,const std::string& problemId) {
    auto root=submissionsRoot(cacheRoot);
    std::vector<Json> items;
    if(problemId.empty()) {
        for(const auto& directory:problemDirectories(root)) {
            auto current=loadDirectory(directory);
            items.insert(items.end(),current.begin(),current.end());
        }
        std::sort(items.begin(),items.end(),[](const Json& a,const Json& b){
            return a.value("id",std::string())>b.value("id",std::string());
        });
    } else items=loadProblem(root,problemId);
    Json result=Json::array();
    for(std::size_t i=0;i<items.size() && i<maxListed;++i) result.push_back(submissionSummary(items[i]));
    return {{"submissions",result}};
}
Json readSubmission(const fs::path& cacheRoot,const std::string& submissionId) {
    if(!safeSegment(submissionId,true) || submissionId.size()<8) throw ApiError(404,"提交记录不存在");
    auto root=submissionsRoot(cacheRoot);
    for(const auto& directory:problemDirectories(root)) {
        auto path=directory/(submissionId+".json");
        std::error_code error;
        if(!fs::is_regular_file(path,error)) continue;
        auto item=Json::parse(readFile(path));
        Json result=submissionSummary(item);
        Json extra={{"source",item.value("source",std::string())},
                    {"groups",item.value("groups",Json::array())},
                    {"cases",item.value("cases",Json::array())},
                    {"compileLog",item.value("compileLog",std::string())},
                    {"message",item.value("message",std::string())},
                    {"durationMs",item.value("durationMs",0LL)},
                    {"improved",item.value("improved",false)},
                    {"previousBest",item.value("previousBest",Json(nullptr))}};
        result.update(extra);
        return result;
    }
    throw ApiError(404,"提交记录不存在");
}
Json bestFor(const fs::path& cacheRoot,const std::string& problemId) {
    auto items=loadProblem(submissionsRoot(cacheRoot),problemId);
    if(items.empty()) return nullptr;
    const Json* best=nullptr;
    for(const auto& item:items)
        if(!best || item.value("score",0LL)>best->value("score",0LL)) best=&item;
    return {{"id",best->value("id",std::string())},{"score",best->value("score",0LL)},
            {"verdict",best->value("verdict",std::string())},{"at",best->value("at",std::string())}};
}
Json problemStats(const fs::path& cacheRoot,const std::string& problemId) {
    return statOf(loadProblem(submissionsRoot(cacheRoot),problemId));
}
long long clearSubmissions(const fs::path& cacheRoot,const std::string& problemId) {
    auto root=submissionsRoot(cacheRoot);
    long long removed=0;
    auto countFiles=[](const fs::path& directory){
        long long count=0; std::error_code error;
        for(const auto& entry:fs::recursive_directory_iterator(directory,error))
            if(entry.is_regular_file() && isSubmissionName(utf8(entry.path().filename().wstring()))) ++count;
        return count;
    };
    if(problemId.empty()) {
        for(const auto& directory:problemDirectories(root)) {
            removed+=countFiles(directory);
            std::error_code error; fs::remove_all(directory,error);
        }
    } else {
        if(!safeSegment(problemId,true)) throw std::runtime_error("题目 id 不合法");
        auto directory=root/wide(problemId);
        removed+=countFiles(directory);
        std::error_code error; fs::remove_all(directory,error);
    }
    return removed;
}
long long removeProblemSubmissions(const fs::path& cacheRoot,const std::string& problemId) { return clearSubmissions(cacheRoot,problemId); }
