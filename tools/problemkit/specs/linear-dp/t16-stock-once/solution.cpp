#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    long long best = 0;
    long long mn = a[0];
    for (long long i = 1; i < n; ++i) {
        long long profit = a[i] - mn;
        if (profit > best) best = profit;
        if (a[i] < mn) mn = a[i];
    }
    return best;
}
