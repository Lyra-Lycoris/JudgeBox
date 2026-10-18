#include<iostream>
#include "process.hpp"

int main(){
    std::cout<<"Judge is Ready!\n";

    auto result = runTask(
        LR"(E:\JudgeBox\build\ExitCode7.exe)",
        L"",
        "",
        1000,
        268435456
    );

    std::cout<< std::boolalpha <<"start:"<<result.started<<'\n'
             <<"exit:"<<result.exit<<'\n'
             <<"error:"<<result.errorMessage<<'\n';

    if(!result.started || !result.errorMessage.empty() || result.exit!=7){
        std::cerr<<"WA on luanch\n";
        return 1;
    }

    auto missing = runTask(//错误案例
        LR"(E:\JudgeBox\build\__missing_program__.exe)",
        L"",
        "",
        1000,
        268435456
    );

    if (missing.started || missing.errorMessage.empty()) {
        std::cerr << "FAIL: expected a launch error\n";
        return 1;
    }

    std::cout<<"pass all test\n";

    return 0;
}