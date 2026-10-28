#include "process.hpp"
#include <windows.h>
#include <algorithm>
#include <chrono>
#include <thread>

namespace {
struct Handle {
    HANDLE h = nullptr;
    explicit Handle(HANDLE value = nullptr) : h(value) {}
    ~Handle() { reset(); }
    Handle(const Handle&) = delete;
    Handle& operator=(const Handle&) = delete;
    void reset(HANDLE value = nullptr) { if (h && h != INVALID_HANDLE_VALUE) CloseHandle(h); h = value; }
    explicit operator bool() const { return h && h != INVALID_HANDLE_VALUE; }
};
std::string winError(const char* what) { return std::string(what) + " (Windows error " + std::to_string(GetLastError()) + ")"; }
std::vector<wchar_t> environmentBlock(const RunOptions& options) {
    std::vector<std::wstring> entries;
    auto original=GetEnvironmentStringsW();
    if(!original) throw std::runtime_error("GetEnvironmentStringsW failed");
    for(auto p=original;*p;p+=wcslen(p)+1) entries.emplace_back(p);
    FreeEnvironmentStringsW(original);
    auto set=[&](const std::wstring& name,const std::wstring& value) {
        auto prefix=name+L"=";
        for(auto& entry:entries) if(_wcsnicmp(entry.c_str(),prefix.c_str(),prefix.size())==0) { entry=prefix+value; return; }
        entries.push_back(prefix+value);
    };
    std::wstring path;
    for(const auto& entry:entries) if(_wcsnicmp(entry.c_str(),L"PATH=",5)==0) path=entry.substr(5);
    std::wstring prepended; for(const auto& dir:options.pathEntries) prepended+=dir+L";";
    set(L"PATH",prepended+path);
    for(const auto& [name,value]:options.environment) {
        if(value.empty()) {
            auto prefix=name+L"=";
            entries.erase(std::remove_if(entries.begin(),entries.end(),[&](const auto& entry){return _wcsnicmp(entry.c_str(),prefix.c_str(),prefix.size())==0;}),entries.end());
        } else set(name,value);
    }
    std::sort(entries.begin(),entries.end(),[](const auto& a,const auto& b){return _wcsicmp(a.c_str(),b.c_str())<0;});
    std::vector<wchar_t> block;
    for(const auto& entry:entries) { block.insert(block.end(),entry.begin(),entry.end()); block.push_back(0); }
    block.push_back(0); return block;
}
bool pipe(Handle& read, Handle& write, bool input, std::string& error) {
    SECURITY_ATTRIBUTES sa{sizeof(sa), nullptr, TRUE};
    if (!CreatePipe(&read.h, &write.h, &sa, 0) ||
        !SetHandleInformation(input ? write.h : read.h, HANDLE_FLAG_INHERIT, 0)) {
        error = winError("Create pipe"); return false;
    }
    return true;
}
runResult execute(const std::wstring& exe, std::wstring command, const std::string& input, const RunOptions& opt) {
    runResult result;
    if (opt.timeMs <= 0 || opt.timeMs > 600000 || opt.memoryBytes < 1024*1024 || !opt.outputBytes) {
        result.errorMessage = "Invalid time/memory/output limit"; return result;
    }
    if (opt.cancel && opt.cancel->load()) { result.cancelled = true; return result; }
    const bool fileInput=!opt.inputPath.empty(),fileOutput=!opt.stdoutPath.empty();
    Handle inRead,inWrite,outRead,outWrite,errRead,errWrite,inputFile,outputFile;
    SECURITY_ATTRIBUTES inherit{sizeof(inherit),nullptr,TRUE};
    if(fileInput) {
        inputFile.reset(CreateFileW(opt.inputPath.c_str(),GENERIC_READ,FILE_SHARE_READ,&inherit,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL|FILE_FLAG_SEQUENTIAL_SCAN,nullptr));
        if(!inputFile) { result.errorMessage=winError("Open input file"); return result; }
    } else if(!pipe(inRead,inWrite,true,result.errorMessage)) return result;
    if(fileOutput) {
        outputFile.reset(CreateFileW(opt.stdoutPath.c_str(),GENERIC_WRITE,FILE_SHARE_READ,&inherit,CREATE_ALWAYS,FILE_ATTRIBUTE_NORMAL|FILE_FLAG_SEQUENTIAL_SCAN,nullptr));
        if(!outputFile) { result.errorMessage=winError("Open output file"); return result; }
    } else if(!pipe(outRead,outWrite,false,result.errorMessage)) return result;
    if(!pipe(errRead,errWrite,false,result.errorMessage)) return result;
    Handle job(CreateJobObjectW(nullptr,nullptr));
    Handle port(CreateIoCompletionPort(INVALID_HANDLE_VALUE,nullptr,0,1));
    if (!job || !port) { result.errorMessage=winError("Create job/completion port"); return result; }
    JOBOBJECT_EXTENDED_LIMIT_INFORMATION limits{};
    limits.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE | JOB_OBJECT_LIMIT_DIE_ON_UNHANDLED_EXCEPTION | JOB_OBJECT_LIMIT_JOB_MEMORY;
    limits.JobMemoryLimit = static_cast<SIZE_T>(opt.memoryBytes);
    JOBOBJECT_ASSOCIATE_COMPLETION_PORT association{job.h,port.h};
    if (!SetInformationJobObject(job.h,JobObjectExtendedLimitInformation,&limits,sizeof(limits)) ||
        !SetInformationJobObject(job.h,JobObjectAssociateCompletionPortInformation,&association,sizeof(association))) {
        result.errorMessage=winError("Set job limits"); return result;
    }
    SIZE_T size=0;
    InitializeProcThreadAttributeList(nullptr,1,0,&size);
    std::vector<unsigned char> storage(size);
    auto attributes=reinterpret_cast<LPPROC_THREAD_ATTRIBUTE_LIST>(storage.data());
    if (!InitializeProcThreadAttributeList(attributes,1,0,&size)) { result.errorMessage=winError("Initialize handle list"); return result; }
    HANDLE inherited[]{fileInput?inputFile.h:inRead.h,fileOutput?outputFile.h:outWrite.h,errWrite.h};
    if (!UpdateProcThreadAttribute(attributes,0,PROC_THREAD_ATTRIBUTE_HANDLE_LIST,inherited,sizeof(inherited),nullptr,nullptr)) {
        result.errorMessage=winError("Restrict handle inheritance"); DeleteProcThreadAttributeList(attributes); return result;
    }
    STARTUPINFOEXW si{}; si.StartupInfo.cb=sizeof(si); si.StartupInfo.dwFlags=STARTF_USESTDHANDLES;
    si.StartupInfo.hStdInput=inherited[0]; si.StartupInfo.hStdOutput=inherited[1]; si.StartupInfo.hStdError=errWrite.h; si.lpAttributeList=attributes;
    PROCESS_INFORMATION pi{};
    auto env=environmentBlock(opt);
    BOOL ok=CreateProcessW(exe.c_str(),command.data(),nullptr,nullptr,TRUE,
        CREATE_SUSPENDED|CREATE_NO_WINDOW|EXTENDED_STARTUPINFO_PRESENT|CREATE_UNICODE_ENVIRONMENT,env.data(),
        opt.workingDirectory.empty()?nullptr:opt.workingDirectory.c_str(),&si.StartupInfo,&pi);
    DeleteProcThreadAttributeList(attributes);
    if (!ok) { result.errorMessage=winError("CreateProcessW"); return result; }
    Handle process(pi.hProcess), mainThread(pi.hThread);
    if (!AssignProcessToJobObject(job.h,process.h)) {
        result.errorMessage=winError("Assign job"); TerminateProcess(process.h,1); WaitForSingleObject(process.h,INFINITE); return result;
    }
    result.started=true;
    inRead.reset(); outWrite.reset(); errWrite.reset(); inputFile.reset();
    std::atomic_size_t captured{0};
    auto readStream=[&](HANDLE h, std::string& target) {
        char buffer[8192]; DWORD count;
        while (ReadFile(h,buffer,sizeof(buffer),&count,nullptr) && count) {
            auto before=captured.fetch_add(count);
            if (before<opt.outputBytes) target.append(buffer,std::min<std::size_t>(count,opt.outputBytes-before));
        }
    };
    auto capturedBytes=[&] {
        if(!fileOutput) return captured.load();
        LARGE_INTEGER bytes{};
        if(!GetFileSizeEx(outputFile.h,&bytes) || bytes.QuadPart<0) return captured.load();
        auto written=static_cast<std::uint64_t>(bytes.QuadPart);
        if(written>opt.outputBytes) return opt.outputBytes+1;
        return captured.load()+static_cast<std::size_t>(written);
    };
    std::thread readerOut,readerErr,writer;
    auto start=std::chrono::steady_clock::now();
    try {
        if(!fileOutput) readerOut=std::thread(readStream,outRead.h,std::ref(result.stdOut));
        readerErr=std::thread(readStream,errRead.h,std::ref(result.errOut));
        if(!fileInput) writer=std::thread([&] {
            std::size_t pos=0; DWORD count;
            while (pos<input.size() && WriteFile(inWrite.h,input.data()+pos,static_cast<DWORD>(std::min<std::size_t>(8192,input.size()-pos)),&count,nullptr) && count) pos+=count;
            inWrite.reset();
        });
        if (ResumeThread(mainThread.h)==static_cast<DWORD>(-1)) result.errorMessage=winError("ResumeThread");
        auto messages=[&](DWORD wait) {
            DWORD message; ULONG_PTR key; LPOVERLAPPED value;
            while (GetQueuedCompletionStatus(port.h,&message,&key,&value,wait)) {
                if (message==JOB_OBJECT_MSG_JOB_MEMORY_LIMIT || message==JOB_OBJECT_MSG_PROCESS_MEMORY_LIMIT) result.MLE=true;
                wait=0;
            }
        };
        while (result.errorMessage.empty()) {
            messages(0);
            if (opt.cancel && opt.cancel->load()) result.cancelled=true;
            if (capturedBytes()>opt.outputBytes) result.OLE=true;
            if (result.MLE || result.OLE || result.cancelled) break;
            DWORD state=WaitForSingleObject(process.h,5);
            if (state==WAIT_OBJECT_0) { messages(20); break; }
            if (state==WAIT_FAILED) { result.errorMessage=winError("WaitForSingleObject"); break; }
            auto elapsed=std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now()-start).count();
            if (elapsed>=opt.timeMs) { result.TLE=true; break; }
        }
        // Wall-clock limits still include scheduling and I/O waits, but reported time
        // uses job CPU accounting so process startup overhead does not dominate short runs.
        TerminateJobObject(job.h,1);
        WaitForSingleObject(process.h,INFINITE);
        DWORD exitCode=0;
        if (!GetExitCodeProcess(process.h,&exitCode)) result.errorMessage=winError("GetExitCodeProcess");
        result.exit=exitCode;
    } catch (const std::exception& e) {
        result.errorMessage=e.what(); TerminateJobObject(job.h,1); WaitForSingleObject(process.h,INFINITE);
    }
    if (writer.joinable()) writer.join();
    if (readerOut.joinable()) readerOut.join();
    if (readerErr.joinable()) readerErr.join();
    if (capturedBytes()>opt.outputBytes) result.OLE=true;
    JOBOBJECT_BASIC_ACCOUNTING_INFORMATION accounting{};
    if (QueryInformationJobObject(job.h,JobObjectBasicAccountingInformation,&accounting,sizeof(accounting),nullptr)) {
        auto ticks=accounting.TotalUserTime.QuadPart;
        result.runTimeMs=static_cast<double>(ticks)/10000.0; // User-mode CPU time; Windows FILETIME uses 100 ns units.
    }
    JOBOBJECT_EXTENDED_LIMIT_INFORMATION stats{};
    if (QueryInformationJobObject(job.h,JobObjectExtendedLimitInformation,&stats,sizeof(stats),nullptr)) result.runMemory=static_cast<long long>(stats.PeakJobMemoryUsed);
    return result;
}
}

std::wstring quoteArgument(const std::wstring& arg) {
    std::wstring out=L"\""; std::size_t slashes=0;
    for (auto c:arg) {
        if (c==L'\\') { ++slashes; continue; }
        if (c==L'"') { out.append(slashes*2+1,L'\\'); out+=c; }
        else { out.append(slashes,L'\\'); out+=c; }
        slashes=0;
    }
    out.append(slashes*2,L'\\'); return out+L'"';
}
runResult runProcess(const std::wstring& exe,const std::vector<std::wstring>& args,const std::string& input,const RunOptions& opt) {
    auto command=quoteArgument(exe); for (const auto& arg:args) command+=L" "+quoteArgument(arg);
    return execute(exe,std::move(command),input,opt);
}
runResult runTask(const std::wstring& exe,const std::wstring& arguments,const std::string& input,const long long& timeMs,const long long& memoryBytes) {
    if(memoryBytes<=0) { runResult result; result.errorMessage="Invalid memory limit"; return result; }
    RunOptions opt; opt.timeMs=timeMs; opt.memoryBytes=memoryBytes; opt.outputBytes=4*1024*1024;
    return execute(exe,quoteArgument(exe)+(arguments.empty()?L"":L" "+arguments),input,opt);
}
