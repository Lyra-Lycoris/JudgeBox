#include <bits/stdc++.h>
using namespace std;

static long long gray(long long n, long long k) {
    if (n == 0) return 0;
    long long half = 1LL << (n - 1);
    if (k < half) return gray(n - 1, k);
    return half + gray(n - 1, 2 * half - 1 - k);
}

long long solve(long long n, long long k) {
    return gray(n, k);
}
