#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, string s) {
    const long long MOD = 1000000007LL;
    long long len = (long long)s.size();
    if (n < len) len = n;
    if (len <= 0) return 0;
    vector<long long> dp((size_t)len + 1, 0);
    long long last[26];
    for (int i = 0; i < 26; ++i) last[i] = -1;
    dp[0] = 1;
    for (long long i = 1; i <= len; ++i) {
        int c = (int)(s[(size_t)(i - 1)] - 'a');
        long long value = 2 * dp[(size_t)(i - 1)] % MOD;
        if (last[c] >= 0) value = (value - dp[(size_t)last[c]] + MOD) % MOD;
        dp[(size_t)i] = value;
        last[c] = i - 1;
    }
    return (dp[(size_t)len] - 1 + MOD) % MOD;
}
