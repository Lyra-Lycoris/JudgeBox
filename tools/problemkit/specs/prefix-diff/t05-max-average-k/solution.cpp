#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long k, const vector<long long>& a) {
    vector<long long> pre(n + 1, 0);
    for (long long i = 0; i < n; ++i) {
        pre[i + 1] = pre[i] + a[i];
    }
    long long lo = -1000000000001LL, hi = 1000000000000LL;
    while (lo + 1 < hi) {
        long long mid = lo + (hi - lo) / 2;
        long long best = 0;
        bool feasible = false;
        for (long long j = k; j <= n; ++j) {
            long long i = j - k;
            long long candidate = pre[i] * 1000 - mid * i;
            if (candidate < best) best = candidate;
            if (pre[j] * 1000 - mid * j >= best) {
                feasible = true;
                break;
            }
        }
        if (feasible) {
            lo = mid;
        } else {
            hi = mid;
        }
    }
    return lo;
}
