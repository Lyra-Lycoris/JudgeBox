#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a, long long x) {
    long long lo = 0, hi = n;
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (a[mid] >= x)
            hi = mid;
        else
            lo = mid + 1;
    }
    return lo;
}
