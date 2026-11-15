    static long solve(long n, long[] p) {
        long[] dp0 = new long[(int) n + 1];
        long[] dp1 = new long[(int) n + 1];
        java.util.Arrays.fill(dp1, 1);
        for (int i = (int) n; i >= 2; --i) {
            int par = (int) p[i - 2];
            dp0[par] += dp1[i];
            dp1[par] += (dp0[i] < dp1[i] ? dp0[i] : dp1[i]);
        }
        return dp0[1] < dp1[1] ? dp0[1] : dp1[1];
    }
