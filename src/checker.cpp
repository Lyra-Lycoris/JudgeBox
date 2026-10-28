#include "checker.hpp"
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <vector>
namespace {
bool space(char c) { return c==' ' || c=='\t' || c=='\n' || c=='\r' || c=='\f' || c=='\v'; }
bool number(const std::string& s,double& v) {
    char* end=nullptr; v=std::strtod(s.c_str(),&end);
    return !s.empty() && end==s.c_str()+s.size() && std::isfinite(v);
}
std::string shortToken(const std::string& s) { return s.size()>100 ? s.substr(0,100)+"…" : s; }
void validate(const std::string& checker,double tolerance) {
    if(checker!="tokens" && checker!="float") throw std::runtime_error("未知比较方式");
    if(!std::isfinite(tolerance) || tolerance<0 || tolerance>1) throw std::runtime_error("浮点容差应在 0 到 1 之间");
}
class StringTokens {
    const std::string& text; std::size_t pos=0;
public:
    explicit StringTokens(const std::string& value):text(value) {}
    bool next(std::string& token) {
        while(pos<text.size() && space(text[pos])) ++pos;
        if(pos==text.size()) return false;
        auto start=pos; while(pos<text.size() && !space(text[pos])) ++pos;
        token.assign(text,start,pos-start); return true;
    }
};
class FileTokens {
    std::ifstream stream;
    std::vector<char> buffer=std::vector<char>(1024*1024);
    std::size_t pos=0,end=0;
    bool refill() {
        stream.read(buffer.data(),static_cast<std::streamsize>(buffer.size()));
        end=static_cast<std::size_t>(stream.gcount()); pos=0;
        if(!end && stream.bad()) throw std::runtime_error("读取答案文件失败");
        return end!=0;
    }
public:
    explicit FileTokens(const fs::path& path):stream(path,std::ios::binary) {
        if(!stream) throw std::runtime_error("无法读取文件："+utf8(path.wstring()));
    }
    bool next(std::string& token) {
        token.clear();
        for(;;) {
            if(pos==end && !refill()) return false;
            if(!space(buffer[pos])) break;
            ++pos;
        }
        for(;;) {
            auto start=pos;
            while(pos<end && !space(buffer[pos])) ++pos;
            token.append(buffer.data()+start,pos-start);
            if(pos<end) return true;
            if(!refill()) return true;
        }
    }
};
template<class A,class B>
Comparison compareTokens(A& a,B& b,const std::string& checker,double tolerance) {
    std::string x,y; std::size_t index=0;
    x.reserve(256); y.reserve(256);
    for(;;) {
        bool ax=a.next(x),by=b.next(y); ++index;
        if(!ax && !by) return {true,"全部 token 一致"};
        if(ax && by) {
            if(x==y) continue;
            double u,v;
            if(checker=="float" && number(x,u) && number(y,v) && std::abs(u-v)<=tolerance*std::max(1.0,std::abs(v))) continue;
        }
        return {false,"第 "+std::to_string(index)+" 个 token：预期「"+(by?shortToken(y):"<EOF>")+"」，实际「"+(ax?shortToken(x):"<EOF>")+"」"};
    }
}
}
Comparison compareOutput(const std::string& actual,const std::string& expected,const std::string& checker,double tolerance) {
    if(checker=="exact") {
        if(actual==expected) return {true,"输出完全一致"};
        std::size_t i=0; while(i<actual.size() && i<expected.size() && actual[i]==expected[i]) ++i;
        return {false,"第 "+std::to_string(i+1)+" 个字节不同（严格比较包括空格和换行）"};
    }
    validate(checker,tolerance);
    StringTokens a(actual),b(expected); return compareTokens(a,b,checker,tolerance);
}
Comparison compareOutputFiles(const fs::path& actual,const fs::path& expected,const std::string& checker,double tolerance) {
    if(checker!="exact") {
        validate(checker,tolerance);
        FileTokens a(actual),b(expected); return compareTokens(a,b,checker,tolerance);
    }
    std::ifstream a(actual,std::ios::binary),b(expected,std::ios::binary);
    if(!a) throw std::runtime_error("无法读取文件："+utf8(actual.wstring()));
    if(!b) throw std::runtime_error("无法读取文件："+utf8(expected.wstring()));
    constexpr std::size_t chunk=1024*1024;
    std::vector<char> x(chunk),y(chunk); std::uint64_t offset=0;
    for(;;) {
        a.read(x.data(),chunk); b.read(y.data(),chunk);
        auto nx=static_cast<std::size_t>(a.gcount()),ny=static_cast<std::size_t>(b.gcount());
        auto common=std::min(nx,ny);
        for(std::size_t i=0;i<common;++i) if(x[i]!=y[i]) return {false,"第 "+std::to_string(offset+i+1)+" 个字节不同（严格比较包括空格和换行）"};
        if(nx!=ny) return {false,"第 "+std::to_string(offset+common+1)+" 个字节不同（严格比较包括空格和换行）"};
        if(!nx) return {true,"输出完全一致"};
        offset+=nx;
        if(a.bad() || b.bad()) throw std::runtime_error("读取答案文件失败");
    }
}
