#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& xs, const vector<long long>& ys) {
    long long total = 0;
    long long px = xs[n - 1];
    long long py = ys[n - 1];
    for (long long i = 0; i < n; ++i) {
        long long cx = xs[i];
        long long cy = ys[i];
        total += px * cy - cx * py;
        px = cx;
        py = cy;
    }
    return total < 0 ? -total : total;
}
