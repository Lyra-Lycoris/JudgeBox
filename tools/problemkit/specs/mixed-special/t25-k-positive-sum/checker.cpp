// SPJ：选手只需输出任意 k 个和为 s 的正整数。
// 平台以 `checker.exe <input> <output> <answer>` 调用。
#include "testlib.h"

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);

    long long s = inf.readLong();
    long long k = inf.readLong();

    long long sum = 0;
    for (long long i = 0; i < k; ++i) {
        long long x = ouf.readLong(1, 1000000000LL, format("a[%lld]", i + 1));
        sum += x;
    }
    if (!ouf.seekEof()) quitf(_wa, "输出多余的内容（应恰好有 %lld 个数）", k);
    if (sum != s) quitf(_wa, "%lld 个数的和为 %lld，应为 %lld", k, sum, s);

    quitf(_ok, "ok");
}
