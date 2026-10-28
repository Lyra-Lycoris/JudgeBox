#include "generator.hpp"
#include "checker.hpp"
#include "dataset.hpp"
#include <iostream>
#include <sstream>
#include <stdexcept>
void check(bool v,const char* m) { if (!v) throw std::runtime_error(m); }
template<class F> void rejects(F f) { bool threw=false; try { f(); } catch (...) { threw=true; } check(threw,"invalid rule accepted"); }
int main() {
 try {
    check(compareOutput("1  2\r\n3","1\n2 3","tokens").equal,"tokens");
    check(!compareOutput("1 2 3","1 2","tokens").equal,"extra token");
    check(!compareOutput("1 ","1","exact").equal,"exact");
    check(compareOutput("1.00000001 word","1 word","float",1e-6).equal,"float");
    check(!compareOutput("nan","1","float").equal,"nan");
    auto files=fs::current_path()/"core-test-files"; fs::remove_all(files); fs::create_directories(files/"nested");
    writeFile(files/"actual.txt","1  2\r\n3"); writeFile(files/"expected.txt","1\n2 3");
    check(compareOutputFiles(files/"actual.txt",files/"expected.txt","tokens").equal,"file tokens");
    check(!compareOutputFiles(files/"actual.txt",files/"expected.txt","exact").equal,"file exact");
    writeFile(files/"actual.txt","1.00000001 word"); writeFile(files/"expected.txt","1 word");
    check(compareOutputFiles(files/"actual.txt",files/"expected.txt","float",1e-6).equal,"file float");
    writeFile(files/"nested"/"01.in","2 3"); writeFile(files/"nested"/"01.ans","5"); writeFile(files/"nested"/"01.out","wrong");
    writeFile(files/"nested"/"02.in","4 5"); writeFile(files/"nested"/"02.out","9");
    auto dataset=loadDataset(utf8(files.wstring()));
    check(dataset.cases.size()==2 && dataset.cases[0].expected.extension()==L".ans","dataset discovery");
    auto summary=datasetSummary(dataset).dump(); check(summary.find("2 3")==std::string::npos,"dataset metadata only");
    auto rule=Json::parse(R"({"steps":[{"type":"int","name":"n","min":2,"max":8},{"type":"array","count":"n","min":-5,"max":5}]})");
    check(generateInput(rule,42,0)==generateInput(rule,42,0),"reproducible");
    std::istringstream s(generateInput(rule,42,0)); int n,x,count=0; s>>n; while(s>>x) { check(x>=-5&&x<=5,"range"); ++count; } check(count==n,"array length");
    check(generateInput(rule,42,0,"min")=="2\n-5 -5\n","min boundary");
    auto tree=Json::parse(R"({"steps":[{"type":"int","name":"n","min":8,"max":8},{"type":"tree","nodes":"n"}]})");
    std::istringstream t(generateInput(tree,9,0)); t>>n; count=0; int a,b; while(t>>a>>b) { check(a>=1&&a<b&&b<=n,"tree"); ++count; } check(count==n-1,"tree edges");
    auto graph=Json::parse(R"({"steps":[{"type":"graph","nodes":4,"edges":6}]})");
    std::istringstream g(generateInput(graph,1,0)); count=0; while(g>>a>>b) { check(a!=b,"self loop"); ++count; } check(count==6,"dense graph");
    rejects([&]{generateInput(Json::parse(R"({"steps":[{"type":"array","count":"missing"}]})"),1,0);});
    rejects([&]{generateInput(Json::parse(R"({"steps":[{"type":"graph","nodes":2,"edges":5}]})"),1,0);});
    rejects([&]{generateInput(Json::parse(R"({"steps":[{"type":"string","length":5,"alphabet":""}]})"),1,0);});
    rejects([&]{generateInput(Json::parse(R"({"steps":[{"type":"array","count":"999999999*999999999"}]})"),1,0);});
    rejects([&]{generateInput(Json::parse(R"({"steps":[{"type":"repeat","count":10000,"steps":[{"type":"repeat","count":10000,"steps":[]}]}]})"),1,0);});
    rejects([&]{generateInput(Json::parse(R"({"steps":[{"type":"int","min":-9223372036854775808,"max":0}]})"),1,0);});
    fs::remove_all(files);
    std::cout<<"core tests passed\n";
 } catch(const std::exception& e) { std::cerr<<e.what()<<'\n'; return 1; }
}
