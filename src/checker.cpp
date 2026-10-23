#include "checker.hpp"
#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <sstream>
#include <stdexcept>
namespace {
bool number(const std::string& s,double& v) {
    char* end=nullptr; v=std::strtod(s.c_str(),&end);
    return !s.empty() && end==s.c_str()+s.size() && std::isfinite(v);
}
std::string shortToken(const std::string& s) { return s.size()>100 ? s.substr(0,100)+"…" : s; }
}
Comparison compareOutput(const std::string& actual,const std::string& expected,const std::string& checker,double tolerance) {
    if (checker=="exact") {
        if (actual==expected) return {true,"输出完全一致"};
        std::size_t i=0; while(i<actual.size() && i<expected.size() && actual[i]==expected[i]) ++i;
        return {false,"第 "+std::to_string(i+1)+" 个字节不同（严格比较包括空格和换行）"};
    }
    if (checker!="tokens" && checker!="float") throw std::runtime_error("未知比较方式");
    if (!std::isfinite(tolerance) || tolerance<0 || tolerance>1) throw std::runtime_error("浮点容差应在 0 到 1 之间");
    std::istringstream a(actual),b(expected); std::string x,y; std::size_t index=0;
    for (;;) {
        bool ax=bool(a>>x),by=bool(b>>y); ++index;
        if (!ax && !by) return {true,"全部 token 一致"};
        if (ax && by) {
            if (x==y) continue;
            double u,v;
            if (checker=="float" && number(x,u) && number(y,v) && std::abs(u-v)<=tolerance*std::max(1.0,std::abs(v))) continue;
        }
        return {false,"第 "+std::to_string(index)+" 个 token：预期「"+(by?shortToken(y):"<EOF>")+"」，实际「"+(ax?shortToken(x):"<EOF>")+"」"};
    }
}
