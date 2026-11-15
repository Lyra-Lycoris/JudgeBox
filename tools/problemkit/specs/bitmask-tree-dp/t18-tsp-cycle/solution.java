    static long solve(long n, long[][] w) {
        final long INF = 1L << 62;
        if (n == 1) return 0;
        int size = 1 << (int) n;
        int full = size - 1;
        long[][] dp = new long[size][(int) n];
        for (long[] row : dp) java.util.Arrays.fill(row, INF);
        dp[1][0] = 0;
        for (int mask = 1; mask < size; mask += 2) {
            int rest = full ^ mask;
            for (int v = 0; v < (int) n; ++v) {
                long cur = dp[mask][v];
                if (cur >= INF) continue;
                for (int u = 0; u < (int) n; ++u) {
                    int bit = 1 << u;
                    if ((rest & bit) == 0) continue;
                    long c = w[v][u];
                    if (c < 0) continue;
                    long val = cur + c;
                    if (val < dp[mask | bit][u]) dp[mask | bit][u] = val;
                }
            }
        }
        long best = INF;
        for (int v = 1; v < (int) n; ++v) {
            long cur = dp[full][v];
            long back = w[v][0];
            if (cur >= INF || back < 0) continue;
            long val = cur + back;
            if (val < best) best = val;
        }
        return best >= INF ? -1 : best;
    }
