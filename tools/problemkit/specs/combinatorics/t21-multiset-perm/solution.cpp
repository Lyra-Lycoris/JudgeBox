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

long long solve(long long n, const vector<long long>& a) {
    const long long MOD = 1000000007LL;
    vector<long long> sorted(a.begin(), a.end());
    sort(sorted.begin(), sorted.end());
    vector<long long> fact(n + 1), invfact(n + 1);
    fact[0] = 1;
    for (long long i = 1; i <= n; ++i) fact[i] = fact[i - 1] * (i % MOD) % MOD;
    invfact[n] = powMod(fact[n], MOD - 2);
    for (long long i = n; i >= 1; --i) invfact[i - 1] = invfact[i] * (i % MOD) % MOD;
    long long answer = fact[n];
    long long i = 0;
    while (i < n) {
        long long j = i;
        while (j < n && sorted[j] == sorted[i]) ++j;
        answer = answer * invfact[j - i] % MOD;
        i = j;
    }
    return answer;
}
