#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long k, const vector<long long>& a) {
    long long total = 0;
    for (long long x : a) total += x;
    long long lo = 0, hi = total / k;
    while (lo < hi) {
        long long mid = (lo + hi + 1) / 2;
        long long cnt = 0, cur = 0;
        for (long long x : a) {
            cur += x;
            if (cur >= mid) {
                ++cnt;
                cur = 0;
                if (cnt >= k) break;
            }
        }
        if (cnt >= k) {
            lo = mid;
        } else {
            hi = mid - 1;
        }
    }
    return lo;
}
