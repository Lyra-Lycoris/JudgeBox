#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, long long k) {
    vector<long long> p;
    p.reserve(n);
    for (long long x = 1; x <= k - 1; ++x) p.push_back(x);
    for (long long x = n; x >= k; --x) p.push_back(x);
    return p;
}
