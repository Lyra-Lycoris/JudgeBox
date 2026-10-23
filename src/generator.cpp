#include "generator.hpp"
#include <algorithm>
#include <cctype>
#include <map>
#include <random>
#include <sstream>
#include <stdexcept>

namespace {
constexpr long long maxNumber=1000000000000LL;
using Variables=std::map<std::string,long long>;
struct Expression {
    const std::string text; const Variables& vars; std::size_t pos=0;
    void space() { while(pos<text.size() && std::isspace(static_cast<unsigned char>(text[pos]))) ++pos; }
    long long bound(long long n) { if (n < -maxNumber || n > maxNumber) throw std::runtime_error("表达式数值过大"); return n; }
    long long factor() {
        space(); if (pos>=text.size()) throw std::runtime_error("不完整的表达式");
        char c=text[pos];
        if (c=='+' || c=='-') { ++pos; auto n=factor(); return c=='-'?-n:n; }
        if (c=='(') { ++pos; auto n=add(); space(); if(pos>=text.size() || text[pos++]!=')') throw std::runtime_error("缺少右括号"); return n; }
        if (std::isdigit(static_cast<unsigned char>(c))) { long long n=0; while(pos<text.size() && std::isdigit(static_cast<unsigned char>(text[pos]))) n=bound(n*10+(text[pos++]-'0')); return n; }
        auto begin=pos; while(pos<text.size() && (std::isalnum(static_cast<unsigned char>(text[pos])) || text[pos]=='_')) ++pos;
        auto name=text.substr(begin,pos-begin); auto it=vars.find(name);
        if(it==vars.end()) throw std::runtime_error("未定义变量或非法表达式："+name);
        return it->second;
    }
    long long multiply() {
        auto a=factor(); for (;;) {
            space(); if(pos>=text.size() || (text[pos]!='*' && text[pos]!='/')) return a;
            char op=text[pos++]; auto b=factor();
            if(op=='*') { if(b && std::abs(a)>maxNumber/std::abs(b)) throw std::runtime_error("表达式乘积过大"); a=bound(a*b); }
            else { if(!b) throw std::runtime_error("表达式除以零"); a/=b; }
        }
    }
    long long add() { auto a=multiply(); for (;;) { space(); if(pos>=text.size() || (text[pos]!='+' && text[pos]!='-')) return a; char op=text[pos++]; auto b=multiply(); a=bound(op=='+'?a+b:a-b); } }
    long long run() { if(text.size()>200) throw std::runtime_error("表达式过长"); auto a=add(); space(); if(pos!=text.size()) throw std::runtime_error("非法表达式："+text); return a; }
};
struct Generator {
    std::mt19937_64 random; Variables vars; std::string strategy,out; std::size_t operations=0,work=0;
    void charge() { if(++operations>100000) throw std::runtime_error("生成步骤与重复次数总量超过 100000"); }
    long long value(const Json& v) {
        if(v.is_number_integer()) {
            if(v.is_number_unsigned() && v.get<std::uint64_t>()>static_cast<std::uint64_t>(maxNumber)) throw std::runtime_error("数值超过 10^12");
            auto n=v.get<long long>(); if(n < -maxNumber || n > maxNumber) throw std::runtime_error("数值超过 10^12"); return n;
        }
        if(v.is_string()) return Expression{v.get<std::string>(),vars}.run();
        throw std::runtime_error("需要整数或变量表达式");
    }
    long long get(const Json& obj,const char* key,long long def) { return obj.contains(key)?value(obj.at(key)):def; }
    long long pick(const Json& node) {
        auto low=get(node,"min",0),high=get(node,"max",100);
        if(low>high) throw std::runtime_error("min 不能大于 max");
        auto n=strategy=="min"?low:strategy=="max"?high:std::uniform_int_distribution<long long>(low,high)(random);
        if(node.contains("name")) { auto name=node.at("name").get<std::string>();
            if(name.empty() || name.size()>40 || !(std::isalpha(static_cast<unsigned char>(name[0])) || name[0]=='_') || !std::all_of(name.begin(),name.end(),[](unsigned char c){return std::isalnum(c)||c=='_';})) throw std::runtime_error("变量名须为英文字母、数字或下划线");
            vars[name]=n;
        }
        return n;
    }
    int count(const Json& node,const char* key,int def,int max=10000) { auto n=get(node,key,def); if(n<0 || n>max) throw std::runtime_error(std::string(key)+" 超出允许范围 0.."+std::to_string(max)); return static_cast<int>(n); }
    void append(const std::string& s) { if(out.size()+s.size()>1024*1024) throw std::runtime_error("单组生成输入超过 1 MiB"); out+=s; }
    void steps(const Json& list,int depth=0) {
        if(depth>12 || !list.is_array()) throw std::runtime_error("steps 必须是数组，嵌套最多 12 层");
        for(const auto& node:list) {
            charge();
            auto type=node.at("type").get<std::string>();
            if(type=="int") { auto n=pick(node); if(node.value("emit",true)) append(std::to_string(n)+"\n"); }
            else if(type=="line") {
                const auto& items=node.at("items"); if(!items.is_array() || items.size()>10000) throw std::runtime_error("line.items 应为数组");
                bool first=true; for(const auto& item:items) { if(!first) append(" "); first=false; append(std::to_string(item.is_object()?pick(item):value(item))); } append("\n");
            } else if(type=="array" || type=="matrix") {
                int rows=type=="matrix"?count(node,"rows",1):1,cols=count(node,type=="matrix"?"cols":"count",5);
                if(static_cast<long long>(rows)*cols>100000) throw std::runtime_error("数组/矩阵最多 100000 个元素");
                for(int r=0;r<rows;++r) { for(int c=0;c<cols;++c) { if(c) append(" "); append(std::to_string(pick(node))); } append("\n"); }
            } else if(type=="string") {
                int n=count(node,"length",8,100000); auto chars=node.value("alphabet",std::string("abc"));
                if(chars.empty() || chars.size()>256 || !std::all_of(chars.begin(),chars.end(),[](unsigned char c){return c>=33 && c<=126;})) throw std::runtime_error("alphabet 需要非空 ASCII 可见字符集");
                for(int i=0;i<n;++i) append(std::string(1,chars[std::uniform_int_distribution<std::size_t>(0,chars.size()-1)(random)]));
                append("\n");
            } else if(type=="repeat") {
                int n=count(node,"count",1); for(int i=0;i<n;++i) { charge(); vars["i"]=i+1; steps(node.at("steps"),depth+1); }
            } else if(type=="literal") append(node.at("text").get<std::string>());
            else if(type=="tree" || type=="graph") {
                int n=count(node,"nodes",5,type=="tree"?10000:1000); if(n<1) throw std::runtime_error("nodes 至少为 1");
                std::vector<std::pair<int,int>> edges;
                if(type=="tree") { for(int v=2;v<=n;++v) edges.emplace_back(std::uniform_int_distribution<int>(1,v-1)(random),v); }
                else {
                    bool directed=node.value("directed",false); int m=count(node,"edges",n-1,100000);
                    if(m>n*(n-1)/(directed?1:2)) throw std::runtime_error("简单图边数超过最大值");
                    if(m) {
                        work+=static_cast<std::size_t>(n)*(n-1)/(directed?1:2);
                        if(work>2000000) throw std::runtime_error("单组图候选边生成工作量超过 2000000");
                        for(int u=1;u<=n;++u) for(int v=directed?1:u+1;v<=n;++v) if(u!=v) edges.emplace_back(u,v);
                        std::shuffle(edges.begin(),edges.end(),random); edges.resize(m);
                    }
                }
                bool weighted=node.value("weighted",false);
                for(auto [u,v]:edges) { append(std::to_string(u)+" "+std::to_string(v)); if(weighted) append(" "+std::to_string(pick(node))); append("\n"); }
            } else throw std::runtime_error("未知生成步骤："+type);
        }
    }
};
}
std::string generateInput(const Json& rule,std::uint64_t seed,int index,const std::string& strategy) {
    if(index<0 || (strategy!="random" && strategy!="min" && strategy!="max" && strategy!="boundary")) throw std::runtime_error("非法生成策略或序号");
    auto mode=strategy=="boundary"?(index%3==0?"min":index%3==1?"max":"random"):strategy.c_str();
    Generator g{std::mt19937_64(seed+static_cast<std::uint64_t>(index)*0x9e3779b97f4a7c15ULL),{},mode,{},0,0};
    g.steps(rule.at("steps")); return g.out;
}
