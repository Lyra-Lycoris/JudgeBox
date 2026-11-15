#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& w, long long d) {
    long long lo = 0, hi = 0;
    for (long long x : w) {
        lo = max(lo, x);
        hi += x;
    }
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        long long days = 1, cur = 0;
        for (long long x : w) {
            if (cur + x > mid) {
                ++days;
                cur = x;
                if (days > d) break;
            } else {
                cur += x;
            }
        }
        if (days <= d)
            hi = mid;
        else
            lo = mid + 1;
    }
    return lo;
}
