#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    long long lo = 0, hi = n - 1;
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (a[mid] > a[hi])
            lo = mid + 1;
        else
            hi = mid;
    }
    return a[lo];
}
