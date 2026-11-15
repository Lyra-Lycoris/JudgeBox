    static long solve(long n, long target, long[] coins) {
        final long MOD = 1000000007L;
        long[] dp = new long[(int) target + 1];
        dp[0] = 1;
        for (int i = 0; i < n; ++i) {
            long c = coins[i];
            if (c > target) continue;
            for (long j = c; j <= target; ++j) {
                dp[(int) j] += dp[(int) (j - c)];
                if (dp[(int) j] >= MOD) dp[(int) j] -= MOD;
            }
        }
        return dp[(int) target] % MOD;
    }
