// SPJ：选手只需输出任意一个前缀最大值个数为 k 的排列。
// 平台以 `checker.exe <input> <output> <answer>` 调用。
#include "testlib.h"

#include <vector>

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);

    long long n = inf.readLong();
    long long k = inf.readLong();

    std::vector<long long> p(n);
    for (int i = 0; i < n; ++i) p[i] = ouf.readLong();
    if (!ouf.seekEof()) quitf(_wa, "输出多余的内容（应恰好有 %lld 个数）", n);

    std::vector<int> seen(n + 1, 0);
    for (int i = 0; i < n; ++i) {
        if (p[i] < 1 || p[i] > n) quitf(_wa, "第 %d 个数 %lld 不在 1..%lld 之内", i + 1, p[i], n);
        if (seen[(int)p[i]]++) quitf(_wa, "数字 %lld 出现了不止一次", p[i]);
    }

    long long best = 0, records = 0;
    for (int i = 0; i < n; ++i) {
        if (p[i] > best) {
            best = p[i];
            ++records;
        }
    }
    if (records != k) quitf(_wa, "前缀最大值个数为 %lld，应为 %lld", records, k);

    quitf(_ok, "ok");
}
