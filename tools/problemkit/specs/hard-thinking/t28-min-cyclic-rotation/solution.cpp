#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& a) {
    long long i = 0, j = 1, k = 0;
    while (i < n && j < n && k < n) {
        long long x = a[(i + k) % n];
        long long y = a[(j + k) % n];
        if (x == y) {
            ++k;
        } else if (x > y) {
            i = i + k + 1;
            if (i == j) ++i;
            k = 0;
        } else {
            j = j + k + 1;
            if (i == j) ++j;
            k = 0;
        }
    }
    long long s = min(i, j);
    if (s >= n) s = 0;
    vector<long long> result(n);
    for (long long t = 0; t < n; ++t) result[t] = a[(s + t) % n];
    return result;
}
