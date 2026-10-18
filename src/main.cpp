#include<iostream>
#include "process.hpp"

int main(){
    std::cout<<"Judge is Ready!\n";

    auto result = runTask(
        LR"(C:\msys64\ucrt64\bin\g++.exe)",
        L"--version",
        "",
        1000,
        268435456
    );

    std::cout<< std::boolalpha <<"start:"<<result.started<<'\n';
    std::cout<<"exit:"<<result.exit<<'\n'; 
    std::cout<<"error:"<<result.errorMessage<<'\n';

    if(!result.started || !result.errorMessage.empty() || result.exit!=0){
        std::cerr<<"WA on launch\n";
        return 1;
    }

    /*auto missing = runTask(//错误案例
        LR"(E:\JudgeBox\build\__missing_program__.exe)",
        L"",
        "",
        1000,
        268435456
    );

    if (missing.started || missing.errorMessage.empty()) {
        std::cerr << "FAIL: expected a launch error\n";
        return 1;
    }*/
    

    std::cout<<"pass all test\n";

    return 0;
}