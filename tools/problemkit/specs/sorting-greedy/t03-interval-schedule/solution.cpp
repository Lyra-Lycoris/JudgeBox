#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& l, const vector<long long>& r) {
    const long long SHIFT = 1000000000LL;
    const long long BASE = 2000000001LL;
    vector<long long> keys(n);
    for (long long i = 0; i < n; ++i) {
        keys[i] = (r[i] + SHIFT) * BASE + (l[i] + SHIFT);
    }
    sort(keys.begin(), keys.end());
    long long answer = 0;
    long long lastEnd = -(1LL << 60);
    for (long long i = 0; i < n; ++i) {
        long long li = keys[i] % BASE - SHIFT;
        long long ri = keys[i] / BASE - SHIFT;
        if (li >= lastEnd) {
            ++answer;
            lastEnd = ri;
        }
    }
    return answer;
}
