    static long solve(long n) {
        final long MOD = 1000000007L;
        long prev2 = 1;
        long prev1 = 1;
        if (n == 0) return prev2;
        for (long i = 2; i <= n; ++i) {
            long cur = (prev1 + prev2) % MOD;
            prev2 = prev1;
            prev1 = cur;
        }
        return prev1;
    }
