#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& l, const vector<long long>& r, long long m) {
    const long long SHIFT = 1000000000LL;
    const long long BASE = 2000000001LL;
    vector<long long> keys(n);
    for (long long i = 0; i < n; ++i) keys[i] = (l[i] + SHIFT) * BASE + (r[i] + SHIFT);
    sort(keys.begin(), keys.end());
    long long i = 0, cur = 0, count = 0;
    while (cur < m) {
        long long best = -1;
        while (i < n && keys[i] / BASE - SHIFT <= cur) {
            long long rr = keys[i] % BASE - SHIFT;
            if (rr > best) best = rr;
            ++i;
        }
        if (best <= cur) return -1;
        cur = best;
        ++count;
    }
    return count;
}
