    static long solve(long n, long[] a) {
        int N = (int) n;
        if (N <= 1) return 0;
        int w = N + 1;
        long[] dp = new long[w * w];
        int[] opt = new int[w * w];
        long[] pre = new long[w];
        for (int i = 1; i <= N; ++i) pre[i] = pre[i - 1] + a[i - 1];
        for (int i = 1; i <= N; ++i) opt[i * w + i] = i;
        for (int length = 2; length <= N; ++length) {
            for (int l = 1; l + length - 1 <= N; ++l) {
                int r = l + length - 1;
                int base = l * w;
                int lo = opt[base + r - 1];
                int hi = opt[(l + 1) * w + r];
                if (hi > r - 1) hi = r - 1;
                long best = -1;
                int bestk = lo;
                for (int k = lo; k <= hi; ++k) {
                    long v = dp[base + k] + dp[(k + 1) * w + r];
                    if (best < 0 || v < best) {
                        best = v;
                        bestk = k;
                    }
                }
                dp[base + r] = best + pre[r] - pre[l - 1];
                opt[base + r] = bestk;
            }
        }
        return dp[w + N];
    }
