#include <bits/stdc++.h>
using namespace std;

long long solve(long long n) {
    const long long MOD = 1000000007LL;
    auto powerMod = [&](long long base, long long exponent) -> long long {
        long long result = 1;
        base %= MOD;
        while (exponent > 0) {
            if (exponent & 1LL) result = result * base % MOD;
            base = base * base % MOD;
            exponent >>= 1;
        }
        return result;
    };

    long long factorialN = 1;
    for (long long i = 2; i <= n; ++i) factorialN = factorialN * i % MOD;
    long long upper = 1;
    for (long long i = n + 1; i <= 2 * n; ++i) upper = upper * i % MOD;

    long long binomial = upper * powerMod(factorialN, MOD - 2) % MOD;
    return binomial * powerMod(n + 1, MOD - 2) % MOD;
}
