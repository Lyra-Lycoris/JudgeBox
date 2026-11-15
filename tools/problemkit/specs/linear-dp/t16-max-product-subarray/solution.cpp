#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    long long best = a[0];
    long long mx = a[0];
    long long mn = a[0];
    for (long long i = 1; i < n; ++i) {
        long long x = a[i];
        long long c1 = mx * x;
        long long c2 = mn * x;
        long long newMax = max({x, c1, c2});
        long long newMin = min({x, c1, c2});
        mx = newMax;
        mn = newMin;
        if (mx > best) best = mx;
    }
    return best;
}
