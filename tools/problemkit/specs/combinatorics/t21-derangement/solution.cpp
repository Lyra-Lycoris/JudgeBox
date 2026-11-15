#include <bits/stdc++.h>
using namespace std;

long long solve(long long n) {
    const long long MOD = 1000000007LL;
    if (n == 0) return 1;
    if (n == 1) return 0;
    long long prev2 = 1;  // D(0)
    long long prev1 = 0;  // D(1)
    for (long long i = 2; i <= n; ++i) {
        long long cur = (i - 1) % MOD * ((prev1 + prev2) % MOD) % MOD;
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}
