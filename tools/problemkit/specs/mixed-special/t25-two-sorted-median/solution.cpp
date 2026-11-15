#include <bits/stdc++.h>
using namespace std;

static long long countLE(const vector<long long>& arr, long long x) {
    return (long long)(upper_bound(arr.begin(), arr.end(), x) - arr.begin());
}

static long long kthSmallest(const vector<long long>& a, const vector<long long>& b, long long t) {
    long long lo = -1000000001LL, hi = 1000000001LL;
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (countLE(a, mid) + countLE(b, mid) >= t) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}

long long solve(long long n, const vector<long long>& a, long long m, const vector<long long>& b) {
    long long total = n + m;
    return kthSmallest(a, b, (total + 1) / 2) + kthSmallest(a, b, (total + 2) / 2);
}
