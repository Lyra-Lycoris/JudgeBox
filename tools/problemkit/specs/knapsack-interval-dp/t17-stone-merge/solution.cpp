#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    if (n <= 1) return 0;
    vector<long long> pre(n + 1, 0);
    for (long long i = 0; i < n; ++i) pre[i + 1] = pre[i] + a[i];
    vector<vector<long long>> dp(n, vector<long long>(n, 0));
    for (long long len = 2; len <= n; ++len) {
        for (long long i = 0; i + len - 1 < n; ++i) {
            long long j = i + len - 1;
            long long best = LLONG_MAX;
            for (long long k = i; k < j; ++k) {
                long long cand = dp[i][k] + dp[k + 1][j];
                if (cand < best) best = cand;
            }
            dp[i][j] = best + pre[j + 1] - pre[i];
        }
    }
    return dp[0][n - 1];
}
