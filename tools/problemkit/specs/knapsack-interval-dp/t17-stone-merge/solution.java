    static long solve(long n, long[] a) {
        if (n <= 1) return 0;
        long[] pre = new long[(int) n + 1];
        for (int i = 0; i < n; ++i) pre[i + 1] = pre[i] + a[i];
        long[][] dp = new long[(int) n][(int) n];
        for (long len = 2; len <= n; ++len) {
            for (long i = 0; i + len - 1 < n; ++i) {
                int ii = (int) i;
                int jj = (int) (i + len - 1);
                long best = Long.MAX_VALUE;
                for (int k = ii; k < jj; ++k) {
                    long cand = dp[ii][k] + dp[k + 1][jj];
                    if (cand < best) best = cand;
                }
                dp[ii][jj] = best + pre[jj + 1] - pre[ii];
            }
        }
        return dp[0][(int) n - 1];
    }
