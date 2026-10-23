#pragma once
#include "data.hpp"
#include <cstdint>
#include <string>
std::string generateInput(const Json& rule,std::uint64_t seed,int index,const std::string& strategy="random");
