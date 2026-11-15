#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a, long long l, long long r) {
    vector<long long> pre(n + 1, 0);
    for (long long i = 0; i < n; ++i) {
        pre[i + 1] = pre[i] + a[i];
    }
    return pre[r] - pre[l - 1];
}
