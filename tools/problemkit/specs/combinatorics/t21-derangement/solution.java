    static long solve(long n) {
        final long MOD = 1000000007L;
        if (n == 0) return 1;
        if (n == 1) return 0;
        long prev2 = 1;
        long prev1 = 0;
        for (long i = 2; i <= n; ++i) {
            long cur = (i - 1) % MOD * ((prev1 + prev2) % MOD) % MOD;
            prev2 = prev1;
            prev1 = cur;
        }
        return prev1;
    }
