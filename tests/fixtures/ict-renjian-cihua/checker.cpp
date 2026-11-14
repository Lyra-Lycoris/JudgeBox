#include "testlib.h"
#include <algorithm>
#include <set>
#include <string>
#include <vector>

namespace {
std::string trimTrailing(std::string text) {
    while (!text.empty() && (text.back() == '\r' || text.back() == ' ' || text.back() == '\t')) text.pop_back();
    return text;
}

// 不能用 readInt() 再 readLine()：readInt 把流留在行尾分隔符之前，随后的 readLine 只会读到空串，
// 整个文件会错位一行。先按行读表头，再按行读解。
std::vector<std::string> readSolutions(InStream& stream, const char* side) {
    auto header = trimTrailing(stream.readLine());
    if (header.empty() || header.size() > 7 ||
        !std::all_of(header.begin(), header.end(), [](char c) { return c >= '0' && c <= '9'; }))
        quitf(_wa, "%s的解数不是非负整数：「%s」", side, header.c_str());
    int count = std::stoi(header);
    std::vector<std::string> result;
    result.reserve(static_cast<std::size_t>(count));
    for (int i = 0; i < count; ++i) result.push_back(trimTrailing(stream.readLine()));
    return result;
}

std::string firstFew(const std::vector<std::string>& items) {
    std::string text;
    for (std::size_t i = 0; i < items.size() && i < 3; ++i) {
        if (i) text += "，";
        text += "「" + items[i] + "」";
    }
    return text;
}
}

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);
    auto expected = readSolutions(ans, "答案");
    auto actual = readSolutions(ouf, "选手输出");
    std::set<std::string> expectedSet(expected.begin(), expected.end());
    if (expectedSet.size() != expected.size()) quitf(_wa, "答案数据自身含有重复解");
    if (actual.size() != expected.size())
        quitf(_wa, "解的个数不符：期望 %d，实际 %d", static_cast<int>(expected.size()), static_cast<int>(actual.size()));
    std::set<std::string> actualSet;
    for (const auto& item : actual)
        if (!actualSet.insert(item).second) quitf(_wa, "输出含有重复解：「%s」", item.c_str());
    std::vector<std::string> missing, extra;
    for (const auto& item : expectedSet) if (!actualSet.count(item)) missing.push_back(item);
    for (const auto& item : actualSet) if (!expectedSet.count(item)) extra.push_back(item);
    if (!missing.empty()) quitf(_wa, "缺少 %d 条解：%s", static_cast<int>(missing.size()), firstFew(missing).c_str());
    if (!extra.empty()) quitf(_wa, "多出 %d 条解：%s", static_cast<int>(extra.size()), firstFew(extra).c_str());
    quitf(_ok, "ok");
}
