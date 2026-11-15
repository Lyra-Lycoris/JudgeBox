#include <bits/stdc++.h>
using namespace std;

static long long powMod(long long base, long long exp) {
    const long long MOD = 1000000007LL;
    long long result = 1;
    base %= MOD;
    while (exp > 0) {
        if (exp & 1LL) result = result * base % MOD;
        base = base * base % MOD;
        exp >>= 1;
    }
    return result;
}

long long solve(long long n, long long k) {
    const long long MOD = 1000000007LL;
    if (k < 0 || k > n) return 0;
    long long kk = k;
    if (kk > n - kk) kk = n - kk;
    long long numerator = 1, denominator = 1;
    for (long long i = 0; i < kk; ++i) {
        numerator = numerator * ((n - i) % MOD) % MOD;
        denominator = denominator * ((i + 1) % MOD) % MOD;
    }
    return numerator * powMod(denominator, MOD - 2) % MOD;
}
