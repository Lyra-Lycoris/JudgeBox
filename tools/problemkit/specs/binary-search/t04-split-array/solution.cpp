#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a, long long k) {
    long long lo = 0, hi = 0;
    for (long long x : a) {
        lo = max(lo, x);
        hi += x;
    }
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        long long parts = 1, cur = 0;
        for (long long x : a) {
            if (cur + x > mid) {
                ++parts;
                cur = x;
                if (parts > k) break;
            } else {
                cur += x;
            }
        }
        if (parts <= k)
            hi = mid;
        else
            lo = mid + 1;
    }
    return lo;
}
