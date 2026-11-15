#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long cap, const vector<long long>& g, const vector<long long>& w,
                const vector<long long>& v) {
    vector<vector<long long>> groups(n + 2);
    for (long long i = 0; i < n; ++i) groups[g[i]].push_back(i);
    vector<long long> dp(cap + 1, 0);
    for (long long key = 1; key <= n; ++key) {
        if (groups[key].empty()) continue;
        vector<long long> ndp = dp;
        for (long long idx : groups[key]) {
            if (w[idx] > cap) continue;
            for (long long j = cap; j >= w[idx]; --j) {
                long long cand = dp[j - w[idx]] + v[idx];
                if (cand > ndp[j]) ndp[j] = cand;
            }
        }
        dp.swap(ndp);
    }
    return dp[cap];
}
