#pragma once
#include <string>
struct Comparison { bool equal; std::string message; };
Comparison compareOutput(const std::string& actual,const std::string& expected,const std::string& checker,double tolerance=1e-6);
