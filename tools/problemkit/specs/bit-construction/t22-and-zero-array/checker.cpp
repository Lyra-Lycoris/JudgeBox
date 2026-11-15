// SPJ：选手输出任意一个合法的构造即可。平台以 `checker.exe <input> <output> <answer>` 调用。
#include "testlib.h"

#include <vector>

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);

    long long n = inf.readLong();
    if (n < 1 || n > 200000) {
        quitf(_fail, "输入不合法：n = %lld", n);
    }

    std::vector<long long> a;
    while (!ouf.seekEof()) {
        a.push_back(ouf.readLong());
    }
    if (static_cast<long long>(a.size()) != n) {
        quitf(_wa, "长度不对：期望 %lld 个数，实际输出 %d 个数", n, static_cast<int>(a.size()));
    }

    for (long long i = 0; i < n; ++i) {
        if (a[i] < 1 || a[i] > 1000000000LL) {
            quitf(_wa, "第 %lld 个数 %lld 不在 [1, 10^9] 内", i + 1, a[i]);
        }
    }
    for (long long i = 0; i + 1 < n; ++i) {
        long long both = a[i] & a[i + 1];
        if (both != 0) {
            quitf(_wa, "第 %lld、%lld 个数的按位与非零：%lld & %lld = %lld",
                  i + 1, i + 2, a[i], a[i + 1], both);
        }
    }

    quitf(_ok, "ok");
}
