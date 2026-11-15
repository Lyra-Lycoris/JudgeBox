// SPJ：选手只需输出任意一个满足行列和要求的 0/1 矩阵。
// 平台以 `checker.exe <input> <output> <answer>` 调用。
#include "testlib.h"

#include <vector>

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);

    long long n = inf.readLong();
    long long m = inf.readLong();

    std::vector<long long> r(n), c(m);
    for (long long i = 0; i < n; ++i) r[(size_t)i] = inf.readLong();
    for (long long j = 0; j < m; ++j) c[(size_t)j] = inf.readLong();

    std::vector<long long> rowSum(n, 0), colSum(m, 0);
    for (long long i = 0; i < n; ++i) {
        for (long long j = 0; j < m; ++j) {
            long long x = ouf.readLong(0LL, 1LL);
            rowSum[(size_t)i] += x;
            colSum[(size_t)j] += x;
        }
    }
    if (!ouf.seekEof()) quitf(_wa, "extra output, exactly %lld values expected", n * m);

    for (long long i = 0; i < n; ++i) {
        if (rowSum[(size_t)i] != r[(size_t)i]) {
            quitf(_wa, "row %lld has sum %lld, expected %lld", i + 1, rowSum[(size_t)i], r[(size_t)i]);
        }
    }
    for (long long j = 0; j < m; ++j) {
        if (colSum[(size_t)j] != c[(size_t)j]) {
            quitf(_wa, "column %lld has sum %lld, expected %lld", j + 1, colSum[(size_t)j], c[(size_t)j]);
        }
    }

    quitf(_ok, "ok");
}
