#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    const long long SHIFT = 1000000000LL;
    const long long BASE = 1048576LL;
    vector<long long> keys(n);
    for (long long i = 0; i < n; ++i) keys[i] = (a[i] + SHIFT) * BASE + i;
    sort(keys.begin(), keys.end());
    vector<long long> perm(n);
    for (long long p = 0; p < n; ++p) perm[keys[p] % BASE] = p + 1;
    vector<long long> tree(n + 1, 0);
    long long total = 0;
    for (long long i = 0; i < n; ++i) {
        long long v = perm[i];
        long long sum = 0;
        for (long long x = v; x > 0; x -= x & (-x)) sum += tree[x];
        total += i - sum;
        for (long long x = v; x <= n; x += x & (-x)) tree[x] += 1;
    }
    return total;
}
