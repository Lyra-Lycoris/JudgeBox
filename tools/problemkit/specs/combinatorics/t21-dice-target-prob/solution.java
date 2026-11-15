    static long solve(long n) {
        final long MOD = 1000000007L;
        final long INV6 = 166666668L;
        int m = (int) n;
        long[] p = new long[m + 1];
        long[] pre = new long[m + 1];
        p[0] = 1;
        pre[0] = 1;
        for (int i = 1; i <= m; ++i) {
            long window = pre[i - 1];
            if (i >= 7) window -= pre[i - 7];
            window %= MOD;
            if (window < 0) window += MOD;
            p[i] = window * INV6 % MOD;
            pre[i] = (pre[i - 1] + p[i]) % MOD;
        }
        return p[m];
    }
