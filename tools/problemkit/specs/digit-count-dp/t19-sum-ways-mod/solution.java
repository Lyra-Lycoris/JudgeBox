    static long solve(long n, long m) {
        final long MOD = 1000000007L;
        if (n <= 0) return 1;
        long limit = Math.min(m, n);
        int size = (int) n;
        long[] dp = new long[size + 1];
        dp[0] = 1;
        long window = 1;
        for (int i = 1; i <= size; ++i) {
            dp[i] = window % MOD;
            long sub = (i >= limit) ? dp[(int) (i - limit)] : 0;
            window = ((window + dp[i] - sub) % MOD + MOD) % MOD;
        }
        return dp[size];
    }
