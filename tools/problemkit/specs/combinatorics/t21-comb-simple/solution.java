    static long powMod(long base, long exp) {
        final long MOD = 1000000007L;
        long result = 1;
        base %= MOD;
        while (exp > 0) {
            if ((exp & 1L) == 1L) result = result * base % MOD;
            base = base * base % MOD;
            exp >>= 1;
        }
        return result;
    }

    static long solve(long n, long k) {
        final long MOD = 1000000007L;
        if (k < 0 || k > n) return 0;
        long kk = k;
        if (kk > n - kk) kk = n - kk;
        long numerator = 1, denominator = 1;
        for (long i = 0; i < kk; ++i) {
            numerator = numerator * ((n - i) % MOD) % MOD;
            denominator = denominator * ((i + 1) % MOD) % MOD;
        }
        return numerator * powMod(denominator, MOD - 2) % MOD;
    }
