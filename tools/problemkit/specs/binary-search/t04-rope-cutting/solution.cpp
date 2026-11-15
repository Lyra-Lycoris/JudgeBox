#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a, long long k) {
    long long lo = 0, hi = 0;
    for (long long x : a) hi = max(hi, x);
    while (lo < hi) {
        long long mid = lo + (hi - lo + 1) / 2;
        long long cnt = 0;
        for (long long x : a) {
            cnt += x / mid;
            if (cnt >= k) break;
        }
        if (cnt >= k)
            lo = mid;
        else
            hi = mid - 1;
    }
    return lo;
}
