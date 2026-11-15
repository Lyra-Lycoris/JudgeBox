#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long m) {
    const long long MOD = 1000000007LL;
    if (n <= 0) return 1;
    if (m > n) m = n;
    vector<long long> dp(n + 1, 0);
    dp[0] = 1;
    long long window = 1;
    for (long long i = 1; i <= n; ++i) {
        dp[i] = window % MOD;
        long long sub = (i >= m) ? dp[i - m] : 0;
        window = ((window + dp[i] - sub) % MOD + MOD) % MOD;
    }
    return dp[n];
}
