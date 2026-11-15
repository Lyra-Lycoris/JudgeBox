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

long long solve(long long n) {
    const long long MOD = 1000000007LL;
    long long answer = (powMod(2, n + 1) - 2) % MOD;
    if (answer < 0) answer += MOD;
    return answer;
}
