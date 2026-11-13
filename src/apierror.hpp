#pragma once
#include "data.hpp"
#include <stdexcept>
// Thrown by the problem layer when the HTTP status matters (404/409). Plain
// std::runtime_error stays 400, which is what the pre-existing routes rely on.
struct ApiError : std::runtime_error {
    int status;
    Json extra; // merged into the response body, e.g. {"details": [...]}
    ApiError(int status,const std::string& message,Json extra=Json::object())
        : std::runtime_error(message),status(status),extra(std::move(extra)) {}
};
