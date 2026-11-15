    static long solve(long n, long m, long[] blocked) {
        final long MOD = 1000000007L;
        int full = 1 << (int) m;
        int[] valid = new int[full];
        int count = 0;
        for (int s = 0; s < full; ++s) {
            if ((s & (s << 1)) == 0) valid[count++] = s;
        }
        boolean[] compat = new boolean[full * count];
        for (int i = 0; i < count; ++i) {
            int a = valid[i];
            for (int j = 0; j < count; ++j) {
                int b = valid[j];
                if ((a & b) == 0 && ((a << 1) & b) == 0 && ((a >> 1) & b) == 0) {
                    compat[i * count + j] = true;
                }
            }
        }
        long[] dp = new long[full];
        int b0 = (int) blocked[0];
        for (int i = 0; i < count; ++i) {
            int a = valid[i];
            if ((a & b0) == 0) dp[a] = 1;
        }
        for (int row = 1; row < (int) n; ++row) {
            int b = (int) blocked[row];
            long[] ndp = new long[full];
            for (int i = 0; i < count; ++i) {
                int a = valid[i];
                if ((a & b) != 0) continue;
                long total = 0;
                int base = i * count;
                for (int j = 0; j < count; ++j) {
                    if (compat[base + j]) total += dp[valid[j]];
                }
                ndp[a] = total % MOD;
            }
            dp = ndp;
        }
        long ans = 0;
        for (int i = 0; i < count; ++i) ans += dp[valid[i]];
        return ans % MOD;
    }
