#include <bits/stdc++.h>
using namespace std;

long long solve(long long x) {
    long long lo = 0, hi = 1000000001LL;
    while (lo + 1 < hi) {
        long long mid = lo + (hi - lo) / 2;
        long long t = 2 * mid - 1;
        if (t * t <= 4 * x * 1000000LL)
            lo = mid;
        else
            hi = mid;
    }
    return lo;
}
