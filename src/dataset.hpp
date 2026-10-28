#pragma once
#include "data.hpp"
#include "files.hpp"
#include <cstdint>
#include <vector>

struct DatasetCase {
    std::string name;
    fs::path input, expected;
    std::uint64_t inputBytes = 0, expectedBytes = 0;
};
struct Dataset {
    fs::path directory;
    std::vector<DatasetCase> cases;
    std::uint64_t totalBytes = 0, maxExpectedBytes = 0;
};
Dataset loadDataset(const std::string& directory);
Json datasetSummary(const Dataset& dataset);
