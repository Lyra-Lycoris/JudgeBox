#include "sync.hpp"
#include "problems.hpp"
#include "process.hpp"
#include <windows.h>
#include <winhttp.h>
#include <atomic>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <functional>
#include <mutex>
#include <thread>
#include <vector>

namespace {
const char* kUserAgent="JudgeBox/1.4 (+https://github.com/Lyra-Lycoris/JudgeBox)";

std::string nowIso() {
    SYSTEMTIME now; GetSystemTime(&now);
    char buffer[64];
    std::snprintf(buffer,sizeof(buffer),"%04d-%02d-%02dT%02d:%02d:%02dZ",now.wYear,now.wMonth,now.wDay,now.wHour,now.wMinute,now.wSecond);
    return buffer;
}

struct HttpResponse {
    int status=0;
    std::string body;
    std::string etag;
    std::string error;
};

std::string httpErrorMessage(DWORD code) {
    std::string detail;
    switch(code) {
        case ERROR_WINHTTP_CANNOT_CONNECT: detail="无法连接（网络不可用？）"; break;
        case ERROR_WINHTTP_TIMEOUT: detail="连接超时"; break;
        case ERROR_WINHTTP_NAME_NOT_RESOLVED: detail="域名解析失败"; break;
        case ERROR_WINHTTP_SECURE_FAILURE: detail="HTTPS 证书校验失败"; break;
        case ERROR_WINHTTP_CONNECTION_ERROR: detail="连接被重置"; break;
        default: detail="网络错误"; break;
    }
    return detail+"（"+std::to_string(code)+"）";
}

struct WinHttpHandle {
    HINTERNET value=nullptr;
    explicit WinHttpHandle(HINTERNET handle=nullptr):value(handle) {}
    ~WinHttpHandle() { if(value) WinHttpCloseHandle(value); }
    WinHttpHandle(const WinHttpHandle&)=delete;
    WinHttpHandle& operator=(const WinHttpHandle&)=delete;
    explicit operator bool() const { return value!=nullptr; }
};

// 发一个 GET；body 超过 maxBytes 会被截断（题库列表只有几十 KB）。
HttpResponse httpGet(const std::string& url,const std::vector<std::pair<std::string,std::string>>& headers,
                     std::size_t maxBytes,std::ostream* sink) {
    HttpResponse response;
    auto wideUrl=wide(url);
    URL_COMPONENTS parts{};
    parts.dwStructSize=sizeof(parts);
    wchar_t host[256]{},target[8192]{};
    parts.lpszHostName=host; parts.dwHostNameLength=255;
    parts.lpszUrlPath=target; parts.dwUrlPathLength=8191;
    if(!WinHttpCrackUrl(wideUrl.c_str(),static_cast<DWORD>(wideUrl.size()),0,&parts)) {
        response.error="地址解析失败";
        return response;
    }
    std::wstring hostName(host,parts.dwHostNameLength);
    std::wstring targetPath(target,parts.dwUrlPathLength);
    if(targetPath.empty()) targetPath=L"/";
    const bool secure=parts.nScheme==INTERNET_SCHEME_HTTPS;
    WinHttpHandle session(WinHttpOpen(L"JudgeBox/1.4",WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,WINHTTP_NO_PROXY_NAME,WINHTTP_NO_PROXY_BYPASS,0));
    if(!session) { response.error=httpErrorMessage(GetLastError()); return response; }
    WinHttpSetTimeouts(session.value,10000,10000,20000,60000);
    WinHttpHandle connect(WinHttpConnect(session.value,hostName.c_str(),parts.nPort,0));
    if(!connect) { response.error=httpErrorMessage(GetLastError()); return response; }
    WinHttpHandle request(WinHttpOpenRequest(connect.value,L"GET",targetPath.c_str(),nullptr,WINHTTP_NO_REFERER,
                                             WINHTTP_DEFAULT_ACCEPT_TYPES,secure?WINHTTP_FLAG_SECURE:0));
    if(!request) { response.error=httpErrorMessage(GetLastError()); return response; }
    DWORD policy=WINHTTP_OPTION_REDIRECT_POLICY_ALWAYS;
    WinHttpSetOption(request.value,WINHTTP_OPTION_REDIRECT_POLICY,&policy,sizeof(policy));
    std::wstring headerText;
    for(const auto& [name,value]:headers) {
        headerText+=wide(name);
        headerText+=L": ";
        headerText+=wide(value);
        headerText+=L"\r\n";
    }
    if(!WinHttpSendRequest(request.value,headerText.empty()?WINHTTP_NO_ADDITIONAL_HEADERS:headerText.c_str(),
                           static_cast<DWORD>(headerText.size()),WINHTTP_NO_REQUEST_DATA,0,0,0)) {
        response.error=httpErrorMessage(GetLastError());
        return response;
    }
    if(!WinHttpReceiveResponse(request.value,nullptr)) {
        response.error=httpErrorMessage(GetLastError());
        return response;
    }
    DWORD status=0,size=sizeof(status);
    WinHttpQueryHeaders(request.value,WINHTTP_QUERY_STATUS_CODE|WINHTTP_QUERY_FLAG_NUMBER,
                        WINHTTP_HEADER_NAME_BY_INDEX,&status,&size,WINHTTP_NO_HEADER_INDEX);
    response.status=static_cast<int>(status);
    wchar_t etag[512]{}; DWORD etagSize=sizeof(etag);
    if(WinHttpQueryHeaders(request.value,WINHTTP_QUERY_ETAG,WINHTTP_HEADER_NAME_BY_INDEX,etag,&etagSize,WINHTTP_NO_HEADER_INDEX))
        response.etag=utf8(std::wstring(etag));
    std::size_t total=0;
    char buffer[64*1024];
    for(;;) {
        DWORD read=0;
        if(!WinHttpReadData(request.value,buffer,sizeof(buffer),&read)) {
            if(!response.error.empty()) break;
            response.error=httpErrorMessage(GetLastError());
            break;
        }
        if(read==0) break;
        if(sink) {
            sink->write(buffer,read);
            if(!*sink) { response.error="写入文件失败"; break; }
        } else {
            response.body.append(buffer,read);
        }
        total+=read;
        if(total>maxBytes) { response.error="响应超过上限"; break; }
    }
    return response;
}

std::mutex stateMutex;
Json state={{"running",false},{"enabled",true},{"added",0},{"updated",0},{"total",0},
            {"error",""},{"checkedAt",""},{"repo",""},{"skipped",0}};
std::atomic_bool started{false};

fs::path syncCacheFile() { return executableDirectory()/L".cache"/L"problemdb"/L"sync.json"; }

Json readSyncCache() {
    try {
        auto path=syncCacheFile();
        if(!fs::is_regular_file(path)) return Json::object();
        return Json::parse(readFile(path));
    } catch(...) { return Json::object(); }
}
void writeSyncCache(const Json& value) {
    try {
        auto path=syncCacheFile();
        std::error_code error;
        fs::create_directories(path.parent_path(),error);
        writeFile(path,value.dump(-1,' ',false,Json::error_handler_t::replace));
    } catch(...) {}
}
void publish(std::function<void(Json&)> mutate) {
    std::lock_guard lock(stateMutex);
    mutate(state);
}

bool endsWithZip(const std::string& name) {
    if(name.size()<4) return false;
    auto tail=name.substr(name.size()-4);
    for(char& c:tail) c=static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
    return tail==".zip";
}

// raw.githubusercontent.com 在部分网络里会让 WinHTTP 卡在 IPv6 上超时（12002）；
// Windows 10+ 自带 curl.exe，用它下载更稳，找不到 curl 时再退回 WinHTTP。
bool findCurl(std::wstring& path) {
    static std::wstring cached;
    static bool checked=false,found=false;
    if(!checked) {
        checked=true;
        wchar_t buffer[32768];
        DWORD length=SearchPathW(nullptr,L"curl.exe",nullptr,32768,buffer,nullptr);
        if(length && length<32768) { cached.assign(buffer,length); found=true; }
    }
    path=cached;
    return found;
}
// 代理刚关掉时，系统里可能还留着 HTTPS_PROXY/ALL_PROXY 环境变量，curl 会连一个已经关掉的
// 代理端口。连续几次「连不上」就直接停用 curl，让后续文件走 WinHTTP（系统代理/直连）。
std::atomic_bool curlUsable{true};
std::atomic_int curlConnectFailures{0};
bool curlDownload(const std::string& url,const fs::path& target) {
    if(!curlUsable.load()) return false;
    std::wstring curl;
    if(!findCurl(curl)) return false;
    RunOptions options;
    options.timeMs=300000;
    options.memoryBytes=512ULL*1024*1024;
    options.outputBytes=64*1024;
    options.workingDirectory=target.parent_path().wstring();
    auto result=runProcess(curl,{L"-sS",L"-L",L"--fail",L"--retry",L"1",L"--connect-timeout",L"10",L"--max-time",L"240",
                                 L"-A",L"JudgeBox/1.4",L"-o",target.wstring(),wide(url)},"",options);
    if(!result.started || result.TLE || result.MLE) return false;
    if(result.exit==0) { curlConnectFailures.store(0); return true; }
    // 5/6/7 = 代理或主机解析/连接失败，28 = 超时
    if(result.exit==5 || result.exit==6 || result.exit==7 || result.exit==28) {
        if(curlConnectFailures.fetch_add(1)+1>=3) curlUsable.store(false);
    }
    return false;
}
// 用 curl 拉一个小文件（题库列表），返回 HTTP 状态码；拿不到返回 -1。
int curlFetch(const std::string& url,const fs::path& target) {
    std::wstring curl;
    if(!findCurl(curl)) return -1;
    RunOptions options;
    options.timeMs=120000;
    options.memoryBytes=512ULL*1024*1024;
    options.outputBytes=64*1024;
    options.workingDirectory=target.parent_path().wstring();
    auto result=runProcess(curl,{L"-sS",L"-L",L"--connect-timeout",L"15",L"--max-time",L"90",
                                 L"-A",L"JudgeBox/1.4",L"-H",L"Accept: application/vnd.github+json",
                                 L"-o",target.wstring(),L"-w",L"%{http_code}",wide(url)},"",options);
    if(!result.started || result.exit || result.stdOut.empty()) return -1;
    try { return std::stoi(result.stdOut); } catch(...) { return -1; }
}

struct RemoteEntry {
    std::string name,url;
    long long size=0;
};
struct Fetched {
    SyncSettings settings;
    std::vector<RemoteEntry> entries;
    long long latencyMs=0;
    bool ok=false;
    std::string error;
};

// 文件名里的非 ASCII 要按 UTF-8 字节百分号编码，Gitee 的 raw 地址才认。
std::string percentEncode(const std::string& text) {
    static const char* hex="0123456789ABCDEF";
    std::string out;
    for(unsigned char c:text) {
        if((c>='A'&&c<='Z')||(c>='a'&&c<='z')||(c>='0'&&c<='9')||c=='-'||c=='_'||c=='.'||c=='~'||c=='/') out+=static_cast<char>(c);
        else { out+='%'; out+=hex[c>>4]; out+=hex[c&15]; }
    }
    return out;
}

// 拉一个源的题库清单：GitHub 用 contents 接口，Gitee 用 git/trees（contents 不给 size）。
Fetched fetchListing(const SyncSettings& settings) {
    Fetched result;
    result.settings=settings;
    std::string url;
    if(settings.kind=="gitee") {
        url=settings.api+"/repos/"+settings.repo+"/git/trees/"+settings.ref+"?recursive=1";
    } else {
        url=settings.api+"/repos/"+settings.repo+"/contents";
        if(!settings.path.empty()) url+="/"+settings.path;
        url+="?ref="+settings.ref;
    }
    std::vector<std::pair<std::string,std::string>> headers={
        {"User-Agent",kUserAgent},
        {"Accept","application/vnd.github+json"}};
    auto started=std::chrono::steady_clock::now();
    auto listing=httpGet(url,headers,8*1024*1024,nullptr);
    std::string body=listing.body;
    if(!listing.error.empty() || listing.status!=200) {
        // WinHTTP 在某些网络下连不上（GitHub 常见是 IPv6 卡住），退回系统自带的 curl.exe 再试一次。
        auto temporary=fs::temp_directory_path()/L"judgebox-sync-list.json";
        auto status=curlFetch(url,temporary);
        if(status>0) {
            try { body=readFile(temporary); } catch(...) { body.clear(); }
            std::error_code cleanup; fs::remove(temporary,cleanup);
            listing.status=status;
            listing.error.clear();
        }
    }
    result.latencyMs=std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now()-started).count();
    if(!listing.error.empty()) { result.error=listing.error; return result; }
    if(listing.status!=200) {
        result.error=(settings.kind=="gitee"?"Gitee 返回 ":"GitHub 返回 ")+std::to_string(listing.status);
        return result;
    }
    Json document;
    try { document=Json::parse(body); }
    catch(...) { result.error="题库列表不是合法 JSON"; return result; }
    if(settings.kind=="gitee") {
        if(!document.is_object() || !document.contains("tree") || !document["tree"].is_array()) { result.error="题库列表格式不正确"; return result; }
        for(const auto& item:document["tree"]) {
            if(!item.is_object()) continue;
            if(item.value("type",std::string())!="blob") continue;
            auto path=item.value("path",std::string());
            if(!endsWithZip(path)) continue;
            auto name=path;
            auto slash=name.find_last_of('/');
            if(slash!=std::string::npos) name=name.substr(slash+1);
            auto size=item.contains("size") && item["size"].is_number()?item["size"].get<long long>():0LL;
            result.entries.push_back({name,"https://gitee.com/"+settings.repo+"/raw/"+settings.ref+"/"+percentEncode(path),size});
        }
    } else {
        if(!document.is_array()) { result.error="题库列表格式不正确"; return result; }
        for(const auto& item:document) {
            if(!item.is_object()) continue;
            if(item.value("type",std::string())!="file") continue;
            auto name=item.value("name",std::string());
            if(!endsWithZip(name)) continue;
            long long size=0;
            if(item.contains("size")) {
                if(item["size"].is_number()) size=item["size"].get<long long>();
                else if(item["size"].is_string()) { try { size=std::stoll(item["size"].get<std::string>()); } catch(...) { size=0; } }
            }
            auto downloadUrl=item.value("download_url",std::string());
            if(downloadUrl.empty()) continue;
            result.entries.push_back({name,downloadUrl,size});
        }
    }
    result.ok=true;
    return result;
}

// 真正干活：并发探测所有源 → 选延迟最低的 → 只下载本地缺失或大小变化的题包（失败换源重试）。
void runSync() {
    auto settings=syncSettings();
    auto cache=readSyncCache();
    auto database=problemDatabase();
    std::error_code error;
    fs::create_directories(database,error);
    publish([&](Json& value) {
        value["repo"]=settings.repo;
        value["path"]=settings.path;
        value["etag"]=cache.value("etag",std::string());
    });
    if(!settings.enabled) {
        publish([](Json& value) { value["running"]=false; value["error"]=""; value["enabled"]=false; });
        return;
    }
    std::vector<SyncSettings> candidates;
    if(settings.sources.empty()) candidates.push_back(settings);
    else candidates=settings.sources;
    std::vector<Fetched> fetched;
    for(const auto& candidate:candidates) {
        auto item=fetchListing(candidate);
        if(item.ok) fetched.push_back(std::move(item));
    }
    if(fetched.empty()) {
        auto message=candidates.empty()?std::string("没有配置题库源"):std::string("所有题库源都连不上");
        publish([&](Json& value) { value["running"]=false; value["error"]=message; value["checkedAt"]=nowIso(); });
        return;
    }
    std::sort(fetched.begin(),fetched.end(),[](const Fetched& a,const Fetched& b){ return a.latencyMs<b.latencyMs; });
    const auto& primary=fetched.front();
    publish([&](Json& value) {
        value["repo"]=primary.settings.repo;
        value["kind"]=primary.settings.kind;
        value["sourceMs"]=primary.latencyMs;
        value["sources"]=static_cast<int>(fetched.size());
    });
    // 所有源的清单合成一张表：同一个题包保留各源的下载地址，
    // **Gitee 地址永远排在前面**（国内用户下新题也走 Gitee），Gitee 上没有时才回退 GitHub。
    struct Candidate {
        std::string url;
        long long size=0;
        bool gitee=false;
    };
    std::map<std::string,std::vector<Candidate>> index;
    for(const auto& source:fetched) {
        bool isGitee=source.settings.kind=="gitee";
        for(const auto& entry:source.entries) {
            auto& list=index[entry.name];
            bool duplicate=false;
            for(const auto& item:list) if(item.url==entry.url) duplicate=true;
            if(!duplicate) list.push_back({entry.url,entry.size,isGitee});
        }
    }
    for(auto& [name,list]:index) {
        (void)name;
        std::stable_sort(list.begin(),list.end(),[](const Candidate& a,const Candidate& b){ return a.gitee && !b.gitee; });
    }
    struct Task {
        std::string name;
        std::vector<std::string> urls;
        long long size=0;
        bool exists=false;
    };
    std::vector<Task> tasks;
    int skipped=0;
    for(const auto& [name,list]:index) {
        long long size=0;
        std::vector<std::string> urls;
        for(const auto& item:list) { urls.push_back(item.url); if(size<=0) size=item.size; }
        std::error_code statError;
        auto target=database/wide(name);
        bool exists=fs::is_regular_file(target,statError);
        if(exists && size>0) {
            auto localSize=static_cast<long long>(fs::file_size(target,statError));
            if(!statError && localSize==size) { ++skipped; continue; }
        }
        tasks.push_back({name,urls,size,exists});
    }
    std::atomic<int> added{0},updated{0},failed{0};
    std::atomic<std::size_t> cursor{0};
    std::mutex errorMutex;
    std::string firstError;
    auto downloadOne=[&](const Task& task) {
        auto target=database/wide(task.name);
        auto temporary=target;
        temporary+=L".part";
        // task.urls 已经按「Gitee 优先」排好；一个地址失败就换下一个。
        const auto& urls=task.urls;
        long long expected=task.size;
        for(int attempt=0;attempt<3;++attempt) {
            if(attempt) std::this_thread::sleep_for(std::chrono::milliseconds(400*attempt));
            std::error_code cleanup; fs::remove(temporary,cleanup);
            std::string failure;
            bool ok=false;
            auto finished=[](const fs::path& path,long long expect) {
                std::error_code code;
                if(!fs::is_regular_file(path,code)) return false;
                if(expect>0 && static_cast<long long>(fs::file_size(path,code))!=expect) return false;
                return true;
            };
            for(const auto& url:urls) {
                if(curlDownload(url,temporary) && finished(temporary,expected)) { ok=true; break; }
                std::ofstream stream(temporary,std::ios::binary);
                if(!stream) { failure="无法写入题库目录"; continue; }
                auto download=httpGet(url,{{"User-Agent",kUserAgent}},256ULL*1024*1024,&stream);
                stream.close();
                if(download.error.empty() && download.status==200 && finished(temporary,expected)) { ok=true; break; }
                failure=download.error.empty()?("HTTP "+std::to_string(download.status)):download.error;
            }
            if(!ok) {
                fs::remove(temporary,cleanup);
                std::lock_guard lock(errorMutex);
                if(firstError.empty()) firstError="下载 "+task.name+" 失败（"+(failure.empty()?"大小不符":failure)+"）";
                continue;
            }
            std::error_code renameError;
            fs::rename(temporary,target,renameError);
            if(renameError) {
                fs::remove(target,renameError);
                renameError.clear();
                fs::rename(temporary,target,renameError);
            }
            if(renameError) {
                std::lock_guard lock(errorMutex);
                if(firstError.empty()) firstError="无法覆盖 "+task.name;
                fs::remove(temporary,renameError);
                continue;
            }
            if(task.exists) ++updated; else ++added;
            publish([&](Json& value) {
                value["added"]=added.load();
                value["updated"]=updated.load();
                value["skipped"]=skipped;
                value["total"]=static_cast<int>(tasks.size())+skipped;
            });
            return;
        }
        ++failed;
    };
    if(!tasks.empty()) {
        // 并发下载：首次装题库是 200 多个文件，串行会把慢链路拖成几十分钟。
        auto workers=static_cast<std::size_t>(std::max(1u,std::min(8u,std::thread::hardware_concurrency())));
        workers=std::min(workers,tasks.size());
        auto work=[&]() {
            for(;;) {
                auto index=cursor.fetch_add(1);
                if(index>=tasks.size()) return;
                downloadOne(tasks[index]);
            }
        };
        std::vector<std::thread> pool;
        for(std::size_t i=1;i<workers;++i) pool.emplace_back(work);
        work();
        for(auto& thread:pool) thread.join();
    }
    Json next={{"checkedAt",nowIso()},{"added",added.load()},{"updated",updated.load()},
               {"source",primary.settings.kind+":"+primary.settings.repo},{"latencyMs",primary.latencyMs}};
    writeSyncCache(next);
    publish([&](Json& value) {
        value["running"]=false;
        value["added"]=added.load();
        value["updated"]=updated.load();
        value["skipped"]=skipped;
        value["failed"]=failed.load();
        value["total"]=added.load()+updated.load()+skipped+failed.load();
        value["checkedAt"]=nowIso();
        value["error"]=failed.load()?firstError:std::string();
    });
}
}

SyncSettings syncSettings() {
    SyncSettings settings;
    bool custom=false;
    std::vector<SyncSettings> explicitSources;
    if(const char* value=std::getenv("JUDGEBOX_SYNC_OFF"); value && *value!='0' && *value!='\0') settings.enabled=false;
    if(const char* value=std::getenv("JUDGEBOX_SYNC_KIND"); value && *value) { settings.kind=value; custom=true; }
    if(const char* value=std::getenv("JUDGEBOX_SYNC_REPO"); value && *value) { settings.repo=value; custom=true; }
    if(const char* value=std::getenv("JUDGEBOX_SYNC_PATH"); value) settings.path=value;
    if(const char* value=std::getenv("JUDGEBOX_SYNC_REF"); value && *value) settings.ref=value;
    if(const char* value=std::getenv("JUDGEBOX_SYNC_API"); value && *value) settings.api=value;
    // ProblemDatabase/.sync.json：关掉同步 / 换仓库 / 指定多个源
    try {
        auto path=problemDatabase()/L".sync.json";
        if(fs::is_regular_file(path)) {
            auto document=Json::parse(readFile(path));
            if(document.contains("enabled")) settings.enabled=document.value("enabled",true);
            if(document.contains("kind") && document["kind"].is_string()) { settings.kind=document["kind"].get<std::string>(); custom=true; }
            if(document.contains("repo") && document["repo"].is_string()) { settings.repo=document["repo"].get<std::string>(); custom=true; }
            if(document.contains("path") && document["path"].is_string()) settings.path=document["path"].get<std::string>();
            if(document.contains("ref") && document["ref"].is_string()) settings.ref=document["ref"].get<std::string>();
            if(document.contains("api") && document["api"].is_string()) settings.api=document["api"].get<std::string>();
            if(document.contains("sources") && document["sources"].is_array()) {
                for(const auto& item:document["sources"]) {
                    if(!item.is_object()) continue;
                    SyncSettings source;
                    source.kind=item.value("kind",std::string("github"));
                    source.repo=item.value("repo",std::string());
                    if(source.repo.empty()) continue;
                    source.path=item.value("path",std::string());
                    source.ref=item.value("ref",std::string(source.kind=="gitee"?"master":"main"));
                    source.api=item.value("api",std::string(source.kind=="gitee"?"https://gitee.com/api/v5":"https://api.github.com"));
                    explicitSources.push_back(source);
                }
            }
        }
    } catch(...) {}
    if(settings.kind=="gitee" && settings.api=="https://api.github.com") settings.api="https://gitee.com/api/v5";
    if(!explicitSources.empty()) {
        settings.sources=explicitSources;
    } else if(!custom) {
        // 默认两个源：GitHub 与 Gitee 镜像，启动时测延迟挑快的那个。
        SyncSettings github;
        github.kind="github"; github.repo="Lyra-Lycoris/JudgeBox-ProblemDatabase";
        github.ref="main"; github.api="https://api.github.com";
        SyncSettings gitee;
        gitee.kind="gitee"; gitee.repo="night-ling114/JudgeBox-ProblemDatabase";
        gitee.ref="main"; gitee.api="https://gitee.com/api/v5";
        settings.sources={github,gitee};
    }
    return settings;
}

void startProblemSync() {
    if(started.exchange(true)) return;
    auto settings=syncSettings();
    publish([&](Json& value) {
        value["enabled"]=settings.enabled;
        value["running"]=settings.enabled;
        value["repo"]=settings.repo;
        value["path"]=settings.path;
        value["added"]=0; value["updated"]=0;
    });
    if(!settings.enabled) return;
    std::thread([]{
        try { runSync(); }
        catch(const std::exception& error) {
            publish([&](Json& value) { value["running"]=false; value["error"]=error.what(); value["checkedAt"]=nowIso(); });
        } catch(...) {
            publish([](Json& value) { value["running"]=false; value["error"]="同步失败"; value["checkedAt"]=nowIso(); });
        }
    }).detach();
}

Json syncStatus() {
    std::lock_guard lock(stateMutex);
    return state;
}
