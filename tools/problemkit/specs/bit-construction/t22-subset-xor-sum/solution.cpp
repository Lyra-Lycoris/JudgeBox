#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    const long long MOD = 1000000007LL;
    long long mask = 0;
    for (long long v : a) mask |= v;
    long long base = 2;
    long long exponent = n - 1;
    long long power = 1;
    while (exponent > 0) {
        if (exponent & 1LL) power = power * base % MOD;
        base = base * base % MOD;
        exponent >>= 1;
    }
    return mask % MOD * power % MOD;
}
