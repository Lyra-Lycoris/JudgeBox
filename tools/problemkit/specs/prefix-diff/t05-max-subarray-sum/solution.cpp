#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    long long best = a[0];
    long long prefix = 0;
    long long minPrefix = 0;
    for (long long i = 0; i < n; ++i) {
        prefix += a[i];
        best = max(best, prefix - minPrefix);
        minPrefix = min(minPrefix, prefix);
    }
    return best;
}
