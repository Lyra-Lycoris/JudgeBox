#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long cap, const vector<long long>& w, const vector<long long>& v,
                const vector<long long>& c) {
    vector<long long> dp(cap + 1, 0);
    for (long long i = 0; i < n; ++i) {
        long long rest = c[i];
        long long block = 1;
        while (rest > 0) {
            long long take = min(block, rest);
            long long bw = w[i] * take;
            long long bv = v[i] * take;
            if (bw <= cap) {
                for (long long j = cap; j >= bw; --j) {
                    long long cand = dp[j - bw] + bv;
                    if (cand > dp[j]) dp[j] = cand;
                }
            }
            rest -= take;
            block *= 2;
        }
    }
    return dp[cap];
}
