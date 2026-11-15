#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long cap, const vector<long long>& w, const vector<long long>& v) {
    vector<long long> dp(cap + 1, 0);
    for (long long i = 0; i < n; ++i) {
        for (long long j = cap; j >= w[i]; --j) {
            long long cand = dp[j - w[i]] + v[i];
            if (cand > dp[j]) dp[j] = cand;
        }
    }
    return dp[cap];
}
