#include <bits/stdc++.h>
using namespace std;

long long solve(long long n) {
    const long long MOD = 1000000007LL;
    long long prev2 = 1;  // f(0)
    long long prev1 = 1;  // f(1)
    if (n == 0) return prev2;
    for (long long i = 2; i <= n; ++i) {
        long long cur = (prev1 + prev2) % MOD;
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}
