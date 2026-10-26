#include <winsock2.h>
#include <ws2tcpip.h>
#include <bcrypt.h>
#include <shellapi.h>
#include "server.hpp"
#include "judge.hpp"
#include "compiler.hpp"
#include "assets.hpp"
#include "editor_asset.hpp"
#include <algorithm>
#include <array>
#include <iostream>
#include <map>
#include <sstream>

namespace {
std::atomic_bool stopping{false};
BOOL WINAPI consoleHandler(DWORD type) { if(type==CTRL_C_EVENT || type==CTRL_CLOSE_EVENT || type==CTRL_BREAK_EVENT) { stopping=true; return TRUE; } return FALSE; }
struct Socket {
    SOCKET value=INVALID_SOCKET;
    explicit Socket(SOCKET s=INVALID_SOCKET):value(s) {}
    ~Socket() { if(value!=INVALID_SOCKET) closesocket(value); }
    Socket(const Socket&)=delete;
};
std::string dump(const Json& j) { return j.dump(-1,' ',false,Json::error_handler_t::replace); }
std::string token() {
    std::array<unsigned char,24> bytes{};
    if(BCryptGenRandom(nullptr,bytes.data(),static_cast<ULONG>(bytes.size()),BCRYPT_USE_SYSTEM_PREFERRED_RNG)!=0) throw std::runtime_error("无法生成会话凭据");
    const char* hex="0123456789abcdef"; std::string s; for(auto b:bytes) { s+=hex[b>>4]; s+=hex[b&15]; } return s;
}
struct Request { std::string method,path,body; std::map<std::string,std::string> headers; };
Request receive(SOCKET s) {
    DWORD timeout=3000; setsockopt(s,SOL_SOCKET,SO_RCVTIMEO,reinterpret_cast<char*>(&timeout),sizeof(timeout));
    setsockopt(s,SOL_SOCKET,SO_SNDTIMEO,reinterpret_cast<char*>(&timeout),sizeof(timeout));
    std::string data; char buffer[16384]; std::size_t end;
    while((end=data.find("\r\n\r\n"))==std::string::npos) {
        int n=recv(s,buffer,sizeof(buffer),0); if(n<=0) throw std::runtime_error("请求中断"); data.append(buffer,n);
        if(data.size()>32768) throw std::runtime_error("请求头过长");
    }
    Request r; std::istringstream lines(data.substr(0,end)); std::string line,version;
    std::getline(lines,line); std::istringstream first(line); first>>r.method>>r.path>>version;
    if(version!="HTTP/1.1" && version!="HTTP/1.0") throw std::runtime_error("无效 HTTP 请求");
    while(std::getline(lines,line)) {
        if(!line.empty() && line.back()=='\r') line.pop_back();
        auto colon=line.find(':'); if(colon==std::string::npos) throw std::runtime_error("无效请求头");
        auto key=line.substr(0,colon),value=line.substr(colon+1);
        std::transform(key.begin(),key.end(),key.begin(),[](unsigned char c){return static_cast<char>(std::tolower(c));});
        while(!value.empty() && value.front()==' ') value.erase(value.begin());
        if(r.headers.contains(key)) throw std::runtime_error("重复请求头");
        r.headers[key]=value;
    }
    if(r.headers.contains("transfer-encoding")) throw std::runtime_error("不支持分块请求");
    std::size_t length=0;
    if(r.headers.contains("content-length")) { std::size_t used=0; auto& raw=r.headers.at("content-length"); length=std::stoull(raw,&used); if(used!=raw.size() || length>20*1024*1024) throw std::runtime_error("请求超过 20 MiB"); }
    r.body=data.substr(end+4);
    while(r.body.size()<length) { int n=recv(s,buffer,static_cast<int>(std::min<std::size_t>(sizeof(buffer),length-r.body.size())),0); if(n<=0) throw std::runtime_error("请求内容中断"); r.body.append(buffer,n); }
    if(r.body.size()>length) r.body.resize(length);
    return r;
}
void respond(SOCKET s,int code,const std::string& content,const std::string& mime="application/json; charset=utf-8") {
    std::string response="HTTP/1.1 "+std::to_string(code)+(code==200?" OK":code==403?" Forbidden":code==404?" Not Found":" Bad Request")+"\r\nContent-Type: "+mime+"\r\nContent-Length: "+std::to_string(content.size())+"\r\nConnection: close\r\nCache-Control: no-store\r\nX-Content-Type-Options: nosniff\r\nReferrer-Policy: no-referrer\r\nContent-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'\r\n\r\n"+content;
    std::size_t offset=0; while(offset<response.size()) { auto n=send(s,response.data()+offset,static_cast<int>(std::min<std::size_t>(response.size()-offset,1024*1024)),0); if(n<=0) break; offset+=n; }
}
}
int serve(const fs::path& dataDirectory,bool openBrowser,unsigned short requestedPort) {
    WSADATA wsa{}; if(WSAStartup(MAKEWORD(2,2),&wsa)) throw std::runtime_error("Winsock 初始化失败");
    struct Cleanup { ~Cleanup(){WSACleanup();} } cleanup;
    Socket listener(socket(AF_INET,SOCK_STREAM,IPPROTO_TCP)); if(listener.value==INVALID_SOCKET) throw std::runtime_error("无法创建监听 socket");
    BOOL exclusive=TRUE; setsockopt(listener.value,SOL_SOCKET,SO_EXCLUSIVEADDRUSE,reinterpret_cast<char*>(&exclusive),sizeof(exclusive));
    sockaddr_in addr{}; addr.sin_family=AF_INET; addr.sin_addr.s_addr=htonl(INADDR_LOOPBACK); addr.sin_port=htons(requestedPort);
    if(bind(listener.value,reinterpret_cast<sockaddr*>(&addr),sizeof(addr)) || listen(listener.value,8)) throw std::runtime_error("端口绑定失败，请检查端口是否被占用");
    int addrSize=sizeof(addr); getsockname(listener.value,reinterpret_cast<sockaddr*>(&addr),&addrSize);
    const std::string host="127.0.0.1:"+std::to_string(ntohs(addr.sin_port)),origin="http://"+host,session=token();
    auto tools=detectTools(); JudgeEngine engine(fs::absolute(dataDirectory),tools);
    SetConsoleCtrlHandler(consoleHandler,TRUE);
    std::cout<<origin<<"/#"<<session<<std::endl;
    std::cout<<"JudgeBox is running locally. Keep this window open. Ctrl+C to stop.\n"<<std::flush;
    if(openBrowser) ShellExecuteW(nullptr,L"open",wide(origin+"/#"+session).c_str(),nullptr,nullptr,SW_SHOWNORMAL);
    while(!stopping.load()) {
        fd_set reads; FD_ZERO(&reads); FD_SET(listener.value,&reads); timeval wait{0,200000};
        if(select(0,&reads,nullptr,nullptr,&wait)<=0) continue;
        Socket client(accept(listener.value,nullptr,nullptr)); if(client.value==INVALID_SOCKET) continue;
        try {
            auto r=receive(client.value);
            if(r.headers["host"]!=host || (r.headers.contains("origin") && r.headers.at("origin")!=origin)) { respond(client.value,403,dump({{"error","禁止跨域请求"}})); continue; }
            if(r.path.starts_with("/api/")) {
                if(r.headers["x-judgebox-token"]!=session) { respond(client.value,403,dump({{"error","会话已失效，请使用启动窗口中的地址打开界面"}})); continue; }
                Json body=Json::object();
                if(r.method=="POST") {
                    if(!r.headers["content-type"].starts_with("application/json")) throw std::runtime_error("请使用 application/json");
                    body=Json::parse(r.body); if(!body.is_object()) throw std::runtime_error("请求应为 JSON 对象");
                }
                Json result;
                if(r.path=="/api/config" && r.method=="GET") result={{"tools",tools},{"version","1.1.1"},{"dataDirectory",utf8(fs::absolute(dataDirectory).wstring())}};
                else if(r.path=="/api/status" && r.method=="GET") result=engine.status();
                else if(r.path=="/api/run" && r.method=="POST") result=engine.start(body);
                else if(r.path=="/api/cancel" && r.method=="POST") { engine.stop(); result={{"ok",true}}; }
                else if(r.path=="/api/generate" && r.method=="POST") result=engine.preview(body);
                else if(r.path.starts_with("/api/case?index=") && r.method=="GET") { auto id=r.path.substr(16); std::size_t used; int i=std::stoi(id,&used); if(used!=id.size()) throw std::runtime_error("无效测试点编号"); result=engine.detail(i); }
                else if(r.path=="/api/draft" && r.method=="GET") { auto path=dataDirectory/"draft.json"; result=fs::exists(path)?Json::parse(readFile(path)):Json::object(); }
                else if(r.path=="/api/draft" && r.method=="POST") { writeFile(dataDirectory/"draft.json",dump(body)); result={{"ok",true}}; }
                else if(r.path=="/api/shutdown" && r.method=="POST") { stopping=true; engine.stop(); result={{"ok",true}}; }
                else if(r.path=="/api/diagnostics" && r.method=="POST") result=diagnoseSource(body.value("source",std::string()),body.value("language",std::string("cpp")),bundledTools(executableDirectory()),fs::absolute(dataDirectory));
                else { respond(client.value,404,dump({{"error","接口不存在"}})); continue; }
                respond(client.value,200,dump(result));
            } else if(r.method=="GET") {
                if(r.path=="/" || r.path=="/index.html") respond(client.value,200,assets::html,"text/html; charset=utf-8");
                else if(r.path=="/style.css") respond(client.value,200,assets::css,"text/css; charset=utf-8");
                else if(r.path=="/app.js") respond(client.value,200,assets::js,"text/javascript; charset=utf-8");
                else if(r.path=="/editor.js") respond(client.value,200,assets::editorJs,"text/javascript; charset=utf-8");
                else if(r.path=="/favicon.svg") respond(client.value,200,assets::icon,"image/svg+xml");
                else respond(client.value,404,"Not found","text/plain");
            } else respond(client.value,404,dump({{"error","接口不存在"}}));
        } catch(const std::exception& e) { respond(client.value,400,dump({{"error",e.what()}})); }
    }
    engine.stop(); SetConsoleCtrlHandler(consoleHandler,FALSE); return 0;
}
