#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    long long best = 0;
    for (long long i = 0; i < n; ++i) {
        long long ai = a[i];
        for (long long j = i + 1; j < n; ++j) {
            long long v = ai ^ a[j];
            if (v > best) best = v;
        }
    }
    return best;
}
