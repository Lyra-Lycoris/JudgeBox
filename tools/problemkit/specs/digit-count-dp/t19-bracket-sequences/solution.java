    static long solve(long n) {
        final long MOD = 1000000007L;
        long factorialN = 1;
        for (long i = 2; i <= n; ++i) factorialN = factorialN * i % MOD;
        long upper = 1;
        for (long i = n + 1; i <= 2 * n; ++i) upper = upper * i % MOD;
        long binomial = upper * modPow(factorialN, MOD - 2, MOD) % MOD;
        return binomial * modPow(n + 1, MOD - 2, MOD) % MOD;
    }

    static long modPow(long base, long exponent, long mod) {
        long result = 1;
        base %= mod;
        while (exponent > 0) {
            if ((exponent & 1L) == 1L) result = result * base % mod;
            base = base * base % mod;
            exponent >>= 1;
        }
        return result;
    }
