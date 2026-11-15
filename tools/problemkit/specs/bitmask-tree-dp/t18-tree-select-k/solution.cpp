#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long k, const vector<long long>& w, const vector<long long>& p) {
    const long long NEG = -(1LL << 62);
    int N = (int)n, K = (int)k;
    vector<vector<long long>> dp((size_t)N + 1, vector<long long>((size_t)K + 1, NEG));
    vector<int> sz((size_t)N + 1, 1);
    for (int i = 1; i <= N; ++i) {
        dp[i][0] = 0;
        dp[i][1] = w[i - 1];
    }
    for (int i = N; i >= 2; --i) {
        int par = (int)p[i - 2];
        int si = min(sz[i], K), sv = min(sz[par], K);
        int lim = min(K, si + sv);
        for (int j = lim; j >= 1; --j) {
            long long best = dp[par][j];
            int lo = max(1, j - sv), hi = min(j - 1, si);
            for (int t = lo; t <= hi; ++t) {
                long long a = dp[par][j - t], b = dp[i][t];
                if (a == NEG || b == NEG) continue;
                long long val = a + b;
                if (val > best) best = val;
            }
            dp[par][j] = best;
        }
        sz[par] += sz[i];
    }
    return dp[1][K];
}
