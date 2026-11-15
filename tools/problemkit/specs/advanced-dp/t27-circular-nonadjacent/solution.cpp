#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    int N = (int)n;
    if (N == 1) return a[0] > 0 ? a[0] : 0;
    auto linear = [&](int lo, int hi) {
        long long p2 = 0, p1 = 0;  // p2 = f_{i-2}, p1 = f_{i-1}
        for (int i = lo; i <= hi; ++i) {
            long long cur = p2 + a[i];
            if (p1 > cur) cur = p1;
            p2 = p1;
            p1 = cur;
        }
        return p1;
    };
    long long r1 = linear(0, N - 2);
    long long r2 = linear(1, N - 1);
    return r1 > r2 ? r1 : r2;
}
