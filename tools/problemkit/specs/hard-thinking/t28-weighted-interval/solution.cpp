#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<vector<long long>>& seg) {
    vector<array<long long, 3>> a(n);
    for (long long i = 0; i < n; ++i) {
        a[i] = {seg[i][1], seg[i][0], seg[i][2]};  // 右端点, 左端点, 权重
    }
    sort(a.begin(), a.end());
    vector<long long> ends(n);
    for (long long i = 0; i < n; ++i) ends[i] = a[i][0];
    vector<long long> dp(n + 1, 0);
    for (long long i = 0; i < n; ++i) {
        long long l = a[i][1], w = a[i][2];
        long long k = lower_bound(ends.begin(), ends.end(), l) - ends.begin();
        long long best = dp[k] + w;
        dp[i + 1] = max(dp[i], best);
    }
    return dp[n];
}
