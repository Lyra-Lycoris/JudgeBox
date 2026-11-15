    static long solve(long n, long[] c) {
        final long INF = 1L << 62;
        int size = 1 << (int) n;
        long[] dp = new long[size];
        java.util.Arrays.fill(dp, INF);
        dp[0] = 0;
        for (int mask = 1; mask < size; ++mask) {
            int low = mask & (-mask);
            int rest = mask ^ low;
            long best = INF;
            int sub = rest;
            while (true) {
                int s = sub | low;
                long v = dp[mask ^ s] + c[s];
                if (v < best) best = v;
                if (sub == 0) break;
                sub = (sub - 1) & rest;
            }
            dp[mask] = best;
        }
        return dp[size - 1];
    }
