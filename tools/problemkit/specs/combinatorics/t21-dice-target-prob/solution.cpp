#include <bits/stdc++.h>
using namespace std;

long long solve(long long n) {
    const long long MOD = 1000000007LL;
    const long long INV6 = 166666668LL;
    vector<long long> p(n + 1, 0), pre(n + 1, 0);
    p[0] = 1;
    pre[0] = 1;
    for (long long i = 1; i <= n; ++i) {
        long long window = pre[i - 1];
        if (i >= 7) window -= pre[i - 7];
        window %= MOD;
        if (window < 0) window += MOD;
        p[i] = window * INV6 % MOD;
        pre[i] = (pre[i - 1] + p[i]) % MOD;
    }
    return p[n];
}
