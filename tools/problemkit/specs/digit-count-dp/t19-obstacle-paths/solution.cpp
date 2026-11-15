#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long m, const vector<vector<long long>>& g) {
    const long long MOD = 1000000007LL;
    vector<long long> dp((size_t)m, 0);
    for (long long i = 0; i < n; ++i) {
        for (long long j = 0; j < m; ++j) {
            if (g[i][j] == 1) {
                dp[j] = 0;
            } else if (i == 0 && j == 0) {
                dp[j] = 1;
            } else {
                long long left = (j > 0) ? dp[j - 1] : 0;
                dp[j] = (dp[j] + left) % MOD;
            }
        }
    }
    return dp[m - 1];
}
