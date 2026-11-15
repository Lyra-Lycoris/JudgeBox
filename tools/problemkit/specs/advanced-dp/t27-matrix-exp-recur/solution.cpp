#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long x, long long y, long long p, long long q) {
    const long long MOD = 1000000007LL;
    if (n == 0) return x % MOD;
    if (n == 1) return y % MOD;
    long long m00 = p % MOD, m01 = q % MOD, m10 = 1, m11 = 0;
    long long r00 = 1, r01 = 0, r10 = 0, r11 = 1;
    long long e = n - 1;
    while (e > 0) {
        if (e & 1LL) {
            long long t00 = (r00 * m00 + r01 * m10) % MOD;
            long long t01 = (r00 * m01 + r01 * m11) % MOD;
            long long t10 = (r10 * m00 + r11 * m10) % MOD;
            long long t11 = (r10 * m01 + r11 * m11) % MOD;
            r00 = t00;
            r01 = t01;
            r10 = t10;
            r11 = t11;
        }
        long long s00 = (m00 * m00 + m01 * m10) % MOD;
        long long s01 = (m00 * m01 + m01 * m11) % MOD;
        long long s10 = (m10 * m00 + m11 * m10) % MOD;
        long long s11 = (m10 * m01 + m11 * m11) % MOD;
        m00 = s00;
        m01 = s01;
        m10 = s10;
        m11 = s11;
        e >>= 1;
    }
    return (r00 * y + r01 * x) % MOD;
}
