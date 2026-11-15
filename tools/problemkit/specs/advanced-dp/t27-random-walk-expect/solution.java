    static long modPow(long base, long exp, long mod) {
        long result = 1 % mod;
        base %= mod;
        while (exp > 0) {
            if ((exp & 1L) != 0) result = result * base % mod;
            base = base * base % mod;
            exp >>= 1;
        }
        return result;
    }

    static long solve(long n, long p, long q) {
        final long MOD = 1000000007L;
        long inv = modPow((p + q) % MOD, MOD - 2, MOD);
        long pa = (p % MOD) * inv % MOD;
        long pb = (q % MOD) * inv % MOD;
        long e1 = 0, e2 = 0, cur = 0;
        for (long i = 0; i < n; ++i) {
            cur = (1 + pa * e1 + pb * e2) % MOD;
            e2 = e1;
            e1 = cur;
        }
        return cur;
    }
