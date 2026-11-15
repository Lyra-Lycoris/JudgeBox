    static long solve(long n, long k, long[] w, long[] p) {
        final long NEG = -(1L << 62);
        int N = (int) n, K = (int) k;
        long[][] dp = new long[N + 1][K + 1];
        for (long[] row : dp) java.util.Arrays.fill(row, NEG);
        int[] sz = new int[N + 1];
        for (int i = 1; i <= N; ++i) {
            sz[i] = 1;
            dp[i][0] = 0;
            dp[i][1] = w[i - 1];
        }
        for (int i = N; i >= 2; --i) {
            int par = (int) p[i - 2];
            int si = Math.min(sz[i], K), sv = Math.min(sz[par], K);
            int lim = Math.min(K, si + sv);
            for (int j = lim; j >= 1; --j) {
                long best = dp[par][j];
                int lo = Math.max(1, j - sv), hi = Math.min(j - 1, si);
                for (int t = lo; t <= hi; ++t) {
                    long a = dp[par][j - t], b = dp[i][t];
                    if (a == NEG || b == NEG) continue;
                    long val = a + b;
                    if (val > best) best = val;
                }
                dp[par][j] = best;
            }
            sz[par] += sz[i];
        }
        return dp[1][K];
    }
