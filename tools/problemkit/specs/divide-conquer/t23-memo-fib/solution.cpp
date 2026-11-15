#include <bits/stdc++.h>
using namespace std;

static const long long MOD = 1000000007LL;

static pair<long long, long long> fibPair(long long n) {
    if (n == 0) return {0, 1};
    auto [a, b] = fibPair(n >> 1);
    long long c = a * ((2 * b - a + MOD) % MOD) % MOD;
    long long d = (a * a + b * b) % MOD;
    if (n & 1) return {d, (c + d) % MOD};
    return {c, d};
}

long long solve(long long n) {
    return fibPair(n).first;
}
