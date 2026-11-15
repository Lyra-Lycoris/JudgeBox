#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<vector<long long>>& w) {
    const long long INF = (1LL << 62);
    if (n == 1) return 0;
    int size = 1 << (int)n;
    int full = size - 1;
    vector<vector<long long>> dp(size, vector<long long>((size_t)n, INF));
    dp[1][0] = 0;
    for (int mask = 1; mask < size; mask += 2) {
        int rest = full ^ mask;
        for (int v = 0; v < (int)n; ++v) {
            long long cur = dp[mask][v];
            if (cur >= INF) continue;
            for (int u = 0; u < (int)n; ++u) {
                int bit = 1 << u;
                if ((rest & bit) == 0) continue;
                long long c = w[v][u];
                if (c < 0) continue;
                long long val = cur + c;
                if (val < dp[mask | bit][u]) dp[mask | bit][u] = val;
            }
        }
    }
    long long best = INF;
    for (int v = 1; v < (int)n; ++v) {
        long long cur = dp[full][v];
        long long back = w[v][0];
        if (cur >= INF || back < 0) continue;
        long long val = cur + back;
        if (val < best) best = val;
    }
    return best >= INF ? -1 : best;
}
