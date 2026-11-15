#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    long long best = a[0];
    long long current = a[0];
    for (long long i = 1; i < n; ++i) {
        current = (current > 0 ? current + a[i] : a[i]);
        if (current > best) best = current;
    }
    return best;
}
