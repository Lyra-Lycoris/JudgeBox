#include <bits/stdc++.h>
using namespace std;

static long long powMod(long long base, long long exp, long long mod) {
    if (exp == 0) return 1 % mod;
    long long half = powMod(base, exp / 2, mod);
    long long result = half * half % mod;
    if (exp & 1) result = result * (base % mod) % mod;
    return result;
}

long long solve(long long a, long long b, long long m) {
    return powMod(a % m, b, m);
}
