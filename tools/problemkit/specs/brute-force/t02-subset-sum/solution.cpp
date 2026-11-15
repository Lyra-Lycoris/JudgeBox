#include <bits/stdc++.h>
using namespace std;

bool solve(long long target, long long n, const vector<long long>& a) {
    vector<long long> sums;
    sums.reserve((size_t)1 << a.size());
    sums.push_back(0);
    for (long long x : a) {
        size_t m = sums.size();
        sums.resize(m * 2);
        for (size_t i = 0; i < m; ++i) sums[m + i] = sums[i] + x;
    }
    for (long long s : sums) {
        if (s == target) return true;
    }
    return false;
}
