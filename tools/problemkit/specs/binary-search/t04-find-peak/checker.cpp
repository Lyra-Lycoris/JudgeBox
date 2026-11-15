// SPJ：选手只需输出任意一个峰值下标。平台以 `checker.exe <input> <output> <answer>` 调用。
#include "testlib.h"

#include <vector>

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);

    int n = inf.readInt();
    std::vector<long long> a(n);
    for (int i = 0; i < n; ++i) a[i] = inf.readLong();

    long long index = ouf.readLong();
    if (index < 0 || index >= n) {
        quitf(_wa, "下标 %lld 越界，应在 0..%d 之内", index, n - 1);
    }

    int i = static_cast<int>(index);
    if (i > 0 && a[i] <= a[i - 1]) {
        quitf(_wa, "下标 %d 不是峰值：a[%d] = %lld <= a[%d] = %lld", i, i, a[i], i - 1, a[i - 1]);
    }
    if (i + 1 < n && a[i] <= a[i + 1]) {
        quitf(_wa, "下标 %d 不是峰值：a[%d] = %lld <= a[%d] = %lld", i, i, a[i], i + 1, a[i + 1]);
    }

    quitf(_ok, "ok");
}
