#include "path_compat.hpp"
#include <shlobj.h>
#include <sddl.h>
#include <winioctl.h>
#include <algorithm>
#include <cstring>
#include <sstream>
#include <vector>
#include <cstdint>

namespace {
bool ascii(const std::wstring& s){return std::all_of(s.begin(),s.end(),[](wchar_t c){return c<128;});}
fs::path knownFolder(REFKNOWNFOLDERID id){
    PWSTR p=nullptr;if(FAILED(SHGetKnownFolderPath(id,KF_FLAG_CREATE,nullptr,&p))) throw std::runtime_error("Cannot locate a toolchain compatibility directory");
    fs::path result(p);CoTaskMemFree(p);return result;
}
fs::path shortDirectory(const fs::path& path){
    wchar_t p[32768];auto n=GetShortPathNameW(path.c_str(),p,32768);return n && n<32768?fs::path(p):path;
}
std::wstring hashName(const std::wstring& name){
    std::uint64_t h=1469598103934665603ULL;for(auto c:name){h^=static_cast<std::uint16_t>(c);h*=1099511628211ULL;}
    std::wostringstream s;s<<std::hex<<h;return s.str();
}
std::wstring uniqueName(){
    GUID id;if(FAILED(CoCreateGuid(&id)))throw std::runtime_error("Cannot create a unique compatibility path");
    wchar_t text[40];if(!StringFromGUID2(id,text,40))throw std::runtime_error("Cannot format a compatibility path");return text;
}
fs::path linkBase(){
    static const fs::path cached=[]()->fs::path{
    auto local=knownFolder(FOLDERID_LocalAppData)/L"JudgeBox"/L"toolchain-links";fs::create_directories(local);
    auto base=shortDirectory(local);if(ascii(base.wstring()))return base;
    // On systems with disabled 8.3 names and a non-ASCII profile, use a per-user private directory.
    auto common=knownFolder(FOLDERID_ProgramData)/(L"JudgeBox-links-"+uniqueName());
    if(!ascii(common.wstring()))throw std::runtime_error("Please choose an ASCII installation/data path; no ASCII compatibility directory is available");
    PSECURITY_DESCRIPTOR descriptor=nullptr;
    if(!ConvertStringSecurityDescriptorToSecurityDescriptorW(L"D:P(A;OICI;FA;;;OW)(A;OICI;FA;;;SY)(A;OICI;FA;;;BA)",SDDL_REVISION_1,&descriptor,nullptr))throw std::runtime_error("Cannot protect the toolchain compatibility directory");
    SECURITY_ATTRIBUTES attributes{sizeof(attributes),descriptor,FALSE};
    BOOL made=CreateDirectoryW(common.c_str(),&attributes);LocalFree(descriptor);
    // Never reuse a predictable/pre-created ProgramData directory, even if it already exists.
    if(!made)throw std::runtime_error("Cannot create a private ASCII compatibility directory; choose an English installation/data path");
    return common;
    }();
    return cached;
}
struct CreationLock {
    HANDLE handle=INVALID_HANDLE_VALUE;OVERLAPPED overlapped{};
    explicit CreationLock(const fs::path& file){
        handle=CreateFileW(file.c_str(),GENERIC_READ|GENERIC_WRITE,FILE_SHARE_READ|FILE_SHARE_WRITE,nullptr,OPEN_ALWAYS,FILE_ATTRIBUTE_NORMAL,nullptr);
        if(handle==INVALID_HANDLE_VALUE)throw std::runtime_error("Cannot open toolchain path lock");
        if(!LockFileEx(handle,LOCKFILE_EXCLUSIVE_LOCK,0,1,0,&overlapped)){CloseHandle(handle);throw std::runtime_error("Cannot lock toolchain path");}
    }
    ~CreationLock(){UnlockFileEx(handle,0,1,0,&overlapped);CloseHandle(handle);}
    CreationLock(const CreationLock&)=delete;
};
std::wstring mountPointTarget(HANDLE handle){
    std::vector<unsigned char> data(MAXIMUM_REPARSE_DATA_BUFFER_SIZE);
    DWORD returned=0;
    if(!DeviceIoControl(handle,FSCTL_GET_REPARSE_POINT,nullptr,0,data.data(),static_cast<DWORD>(data.size()),&returned,nullptr) || returned<16) return {};
    DWORD tag=0; std::memcpy(&tag,data.data(),sizeof(tag));
    if(tag!=IO_REPARSE_TAG_MOUNT_POINT) return {};
    USHORT offset=0,length=0; std::memcpy(&offset,data.data()+8,sizeof(offset)); std::memcpy(&length,data.data()+10,sizeof(length));
    if(length<2 || length%2 || static_cast<DWORD>(16)+offset+length>returned) return {};
    std::wstring name(reinterpret_cast<const wchar_t*>(data.data()+16+offset),length/2);
    while(!name.empty() && name.back()==L'\0') name.pop_back();
    if(name.rfind(L"\\??\\",0)==0) name.erase(0,4);
    return name;
}
std::wstring normalizedPath(const std::wstring& value){
    std::wstring text=fs::absolute(fs::path(value)).lexically_normal().wstring();
    while(text.size()>3 && (text.back()==L'\\' || text.back()==L'/')) text.pop_back();
    for(auto& c:text) c=towlower(c);
    return text;
}
void junction(const fs::path& alias,const fs::path& target){
    CreationLock lock(fs::path(alias.wstring()+L".lock"));
    HANDLE existing=CreateFileW(alias.c_str(),FILE_READ_ATTRIBUTES,FILE_SHARE_READ|FILE_SHARE_WRITE|FILE_SHARE_DELETE,nullptr,OPEN_EXISTING,FILE_FLAG_OPEN_REPARSE_POINT|FILE_FLAG_BACKUP_SEMANTICS,nullptr);
    if(existing!=INVALID_HANDLE_VALUE){
        auto current=mountPointTarget(existing); CloseHandle(existing);
        // libstdc++ filesystem::equivalent does not identify a directory junction with its target.
        if(!current.empty() && normalizedPath(current)==normalizedPath(target.wstring())) return;
        if(!current.empty() || !RemoveDirectoryW(alias.c_str())) throw std::runtime_error("Toolchain compatibility path already points to a different directory");
    }
    if(!CreateDirectoryW(alias.c_str(),nullptr))throw std::runtime_error("Cannot create toolchain junction directory");
    HANDLE handle=CreateFileW(alias.c_str(),GENERIC_WRITE,0,nullptr,OPEN_EXISTING,FILE_FLAG_OPEN_REPARSE_POINT|FILE_FLAG_BACKUP_SEMANTICS,nullptr);
    if(handle==INVALID_HANDLE_VALUE){RemoveDirectoryW(alias.c_str());throw std::runtime_error("Cannot open toolchain junction directory");}
    auto substitute=L"\\??\\"+target.wstring(),print=target.wstring();
    const auto bufferBytes=(substitute.size()+1+print.size()+1)*sizeof(wchar_t);
    if(bufferBytes+16>MAXIMUM_REPARSE_DATA_BUFFER_SIZE){CloseHandle(handle);RemoveDirectoryW(alias.c_str());throw std::runtime_error("Toolchain compatibility target path is too long");}
    std::vector<unsigned char> data(16+bufferBytes,0);
    auto dword=[&](std::size_t at,DWORD n){std::memcpy(data.data()+at,&n,sizeof(n));};
    auto word=[&](std::size_t at,WORD n){std::memcpy(data.data()+at,&n,sizeof(n));};
    dword(0,IO_REPARSE_TAG_MOUNT_POINT);word(4,static_cast<WORD>(8+bufferBytes));
    word(8,0);word(10,static_cast<WORD>(substitute.size()*2));word(12,static_cast<WORD>((substitute.size()+1)*2));word(14,static_cast<WORD>(print.size()*2));
    std::memcpy(data.data()+16,substitute.c_str(),(substitute.size()+1)*2);
    std::memcpy(data.data()+16+(substitute.size()+1)*2,print.c_str(),(print.size()+1)*2);
    DWORD returned;BOOL ok=DeviceIoControl(handle,FSCTL_SET_REPARSE_POINT,data.data(),static_cast<DWORD>(data.size()),nullptr,0,&returned,nullptr);
    DWORD error=GetLastError();CloseHandle(handle);
    if(!ok){RemoveDirectoryW(alias.c_str());throw std::runtime_error("Cannot create toolchain junction (Windows error "+std::to_string(error)+")");}
}
}
fs::path asciiDirectory(const fs::path& directory){
    auto full=fs::absolute(directory).lexically_normal();if(ascii(full.wstring()))return full;
    auto shortName=shortDirectory(full);if(ascii(shortName.wstring()))return shortName;
    auto alias=linkBase()/hashName(full.wstring());junction(alias,full);return alias;
}
