// SPJ：选手只需输出任意一个使相邻元素差绝对值之和达到最大的 1..n 排列。
// 平台以 `checker.exe <input> <output> <answer>` 调用。
#include "testlib.h"

#include <vector>

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);

    long long n = inf.readLong();

    std::vector<long long> p(n);
    for (int i = 0; i < n; ++i) p[i] = ouf.readLong();
    if (!ouf.seekEof()) quitf(_wa, "输出多余的内容（应恰好有 %lld 个数）", n);

    std::vector<int> seen(n + 1, 0);
    for (int i = 0; i < n; ++i) {
        if (p[i] < 1 || p[i] > n) quitf(_wa, "第 %d 个数 %lld 不在 1..%lld 之内", i + 1, p[i], n);
        if (seen[(int)p[i]]++) quitf(_wa, "数字 %lld 出现了不止一次", p[i]);
    }

    long long sum = 0;
    for (int i = 0; i + 1 < n; ++i) sum += p[i] > p[i + 1] ? p[i] - p[i + 1] : p[i + 1] - p[i];

    long long best = n == 1 ? 0 : n * n / 2 - 1;
    if (sum != best) quitf(_wa, "相邻差之和为 %lld，最大值为 %lld", sum, best);

    quitf(_ok, "ok");
}
