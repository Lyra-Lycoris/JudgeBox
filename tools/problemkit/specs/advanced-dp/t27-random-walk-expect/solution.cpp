#include <bits/stdc++.h>
using namespace std;

static long long modPow(long long base, long long exp, long long mod) {
    long long result = 1 % mod;
    base %= mod;
    while (exp > 0) {
        if (exp & 1LL) result = result * base % mod;
        base = base * base % mod;
        exp >>= 1;
    }
    return result;
}

long long solve(long long n, long long p, long long q) {
    const long long MOD = 1000000007LL;
    long long inv = modPow((p + q) % MOD, MOD - 2, MOD);
    long long pa = (p % MOD) * inv % MOD;
    long long pb = (q % MOD) * inv % MOD;
    long long e1 = 0, e2 = 0, cur = 0;
    for (long long i = 0; i < n; ++i) {
        cur = (1 + pa * e1 + pb * e2) % MOD;
        e2 = e1;
        e1 = cur;
    }
    return cur;
}
