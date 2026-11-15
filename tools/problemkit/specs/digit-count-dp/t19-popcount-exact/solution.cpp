#include <bits/stdc++.h>
using namespace std;

long long solve(long long l, long long r, long long k) {
    static long long comb[62][62];
    for (int i = 0; i < 62; ++i) {
        comb[i][0] = 1;
        for (int j = 1; j <= i; ++j) comb[i][j] = comb[i - 1][j - 1] + comb[i - 1][j];
        for (int j = i + 1; j < 62; ++j) comb[i][j] = 0;
    }

    auto countUpTo = [&](long long x) -> long long {
        if (x < 0 || k < 0) return 0;
        long long res = 0;
        long long used = 0;
        bool ok = true;
        for (int bit = 60; bit >= 0; --bit) {
            if (((x >> bit) & 1LL) != 0) {
                long long need = k - used;
                if (need >= 0 && need <= bit) res += comb[bit][need];
                used += 1;
                if (used > k) {
                    ok = false;
                    break;
                }
            }
        }
        if (ok && used == k) res += 1;
        return res;
    };

    return countUpTo(r) - countUpTo(l - 1);
}
