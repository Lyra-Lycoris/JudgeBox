    static long solve(long n, long[] w, long[] p) {
        long[] dp0 = new long[(int) n + 1];
        long[] dp1 = new long[(int) n + 1];
        for (int i = 1; i <= (int) n; ++i) dp1[i] = w[i - 1];
        for (int i = (int) n; i >= 2; --i) {
            int par = (int) p[i - 2];
            long a = dp0[i], b = dp1[i];
            dp0[par] += (a > b ? a : b);
            dp1[par] += a;
        }
        return dp0[1] > dp1[1] ? dp0[1] : dp1[1];
    }
