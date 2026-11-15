#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long target, const vector<long long>& coins) {
    const long long MOD = 1000000007LL;
    vector<long long> dp(target + 1, 0);
    dp[0] = 1;
    for (long long i = 0; i < n; ++i) {
        long long c = coins[i];
        if (c > target) continue;
        for (long long j = c; j <= target; ++j) {
            dp[j] += dp[j - c];
            if (dp[j] >= MOD) dp[j] -= MOD;
        }
    }
    return dp[target] % MOD;
}
