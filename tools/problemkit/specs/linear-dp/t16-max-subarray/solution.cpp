#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    long long best = a[0];
    long long cur = a[0];
    for (long long i = 1; i < n; ++i) {
        long long x = a[i];
        cur = (cur > 0 ? cur + x : x);
        if (cur > best) best = cur;
    }
    return best;
}
