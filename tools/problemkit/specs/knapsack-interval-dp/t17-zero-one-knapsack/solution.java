    static long solve(long n, long cap, long[] w, long[] v) {
        long[] dp = new long[(int) cap + 1];
        for (int i = 0; i < n; ++i) {
            for (long j = cap; j >= w[i]; --j) {
                long cand = dp[(int) (j - w[i])] + v[i];
                if (cand > dp[(int) j]) dp[(int) j] = cand;
            }
        }
        return dp[(int) cap];
    }
