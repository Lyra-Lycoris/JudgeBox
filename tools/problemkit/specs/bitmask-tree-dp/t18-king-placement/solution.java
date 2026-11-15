    static long solve(long n, long m) {
        if (n < m) {
            long t = n;
            n = m;
            m = t;
        }
        int rows = (int) n, cols = (int) m;
        int size = 1 << cols;
        int[] valid = new int[size];
        int cnt = 0;
        for (int mask = 0; mask < size; ++mask)
            if ((mask & (mask << 1)) == 0) valid[cnt++] = mask;
        long[] dp = new long[size];
        long[] ndp = new long[size];
        for (int i = 0; i < cnt; ++i) dp[valid[i]] = 1;
        for (int r = 1; r < rows; ++r) {
            java.util.Arrays.fill(ndp, 0);
            for (int i = 0; i < cnt; ++i) {
                int a = valid[i];
                long sum = 0;
                for (int j = 0; j < cnt; ++j) {
                    int b = valid[j];
                    if ((a & b) == 0 && (a & (b << 1)) == 0 && ((a << 1) & b) == 0) sum += dp[b];
                }
                ndp[a] = sum;
            }
            long[] tmp = dp;
            dp = ndp;
            ndp = tmp;
        }
        long total = 0;
        for (int i = 0; i < cnt; ++i) total += dp[valid[i]];
        return total;
    }
