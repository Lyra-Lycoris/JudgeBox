#pragma once
#include "files.hpp"
#include <functional>

struct ServeHooks {
    std::function<void(const std::string&)> ready;
    std::function<void()> stopped;
    bool quiet = false;
};

int serve(const fs::path& dataDirectory,bool openBrowser,unsigned short port=0,const ServeHooks& hooks=ServeHooks());
void requestServerStop();
