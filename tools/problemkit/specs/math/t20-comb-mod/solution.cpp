#include <bits/stdc++.h>
using namespace std;

long long mod_pow(long long base, long long exp, long long mod) {
    long long result = 1 % mod;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) result = result * base % mod;
        base = base * base % mod;
        exp >>= 1;
    }
    return result;
}

long long solve(long long n, long long k, long long p) {
    if (k < 0 || k > n) return 0;
    if (k > n - k) k = n - k;
    long long numerator = 1;
    long long denominator = 1;
    for (long long i = 1; i <= k; ++i) {
        numerator = numerator * ((n - k + i) % p) % p;
        denominator = denominator * (i % p) % p;
    }
    return numerator * mod_pow(denominator, p - 2, p) % p;
}
