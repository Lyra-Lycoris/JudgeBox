#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& c) {
    const long long INF = (1LL << 62);
    int size = 1 << (int)n;
    vector<long long> dp(size, INF);
    dp[0] = 0;
    for (int mask = 1; mask < size; ++mask) {
        int low = mask & (-mask);
        int rest = mask ^ low;
        long long best = INF;
        for (int sub = rest;; sub = (sub - 1) & rest) {
            int s = sub | low;
            long long v = dp[mask ^ s] + c[s];
            if (v < best) best = v;
            if (sub == 0) break;
        }
        dp[mask] = best;
    }
    return dp[size - 1];
}
