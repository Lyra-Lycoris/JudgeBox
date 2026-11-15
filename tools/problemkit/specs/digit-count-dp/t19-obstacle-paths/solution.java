    static long solve(long n, long m, long[][] g) {
        final long MOD = 1000000007L;
        int rows = (int) n;
        int cols = (int) m;
        long[] dp = new long[cols];
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols; ++j) {
                if (g[i][j] == 1) {
                    dp[j] = 0;
                } else if (i == 0 && j == 0) {
                    dp[j] = 1;
                } else {
                    long left = (j > 0) ? dp[j - 1] : 0;
                    dp[j] = (dp[j] + left) % MOD;
                }
            }
        }
        return dp[cols - 1];
    }
