// SPJ：选手只需输出任意一个行列和都满足要求的非负整数矩阵。
// 平台以 `checker.exe <input> <output> <answer>` 调用。
#include "testlib.h"

#include <vector>

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);

    long long n = inf.readLong();
    long long m = inf.readLong();

    std::vector<long long> r(n), c(m);
    for (int i = 0; i < n; ++i) r[i] = inf.readLong();
    for (int j = 0; j < m; ++j) c[j] = inf.readLong();

    std::vector<long long> rowSum(n, 0), colSum(m, 0);
    for (long long i = 0; i < n; ++i) {
        for (long long j = 0; j < m; ++j) {
            long long x = ouf.readLong(0, 1000000000LL);
            rowSum[(int)i] += x;
            colSum[(int)j] += x;
        }
    }
    if (!ouf.seekEof()) quitf(_wa, "输出多余的内容（应恰好有 %lld 个数）", n * m);

    for (long long i = 0; i < n; ++i) {
        if (rowSum[(int)i] != r[(int)i]) {
            quitf(_wa, "第 %lld 行的元素和为 %lld，应为 %lld", i + 1, rowSum[(int)i], r[(int)i]);
        }
    }
    for (long long j = 0; j < m; ++j) {
        if (colSum[(int)j] != c[(int)j]) {
            quitf(_wa, "第 %lld 列的元素和为 %lld，应为 %lld", j + 1, colSum[(int)j], c[(int)j]);
        }
    }

    quitf(_ok, "ok");
}
