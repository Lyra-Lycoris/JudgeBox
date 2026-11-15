#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a, long long k) {
    if (k <= 1) return 0;
    vector<long long> b = a;
    sort(b.begin(), b.end());
    long long lo = 0, hi = (b[n - 1] - b[0]) / (k - 1);
    while (lo < hi) {
        long long mid = (lo + hi + 1) / 2;
        long long cnt = 1, last = b[0];
        for (long long i = 1; i < n; ++i) {
            if (b[i] - last >= mid) {
                ++cnt;
                last = b[i];
                if (cnt >= k) break;
            }
        }
        if (cnt >= k) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}
