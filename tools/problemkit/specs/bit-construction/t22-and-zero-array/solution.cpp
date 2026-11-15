#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n) {
    vector<long long> a(n);
    for (long long i = 0; i < n; ++i) a[i] = (i % 2 == 0) ? 1 : 2;
    return a;
}
