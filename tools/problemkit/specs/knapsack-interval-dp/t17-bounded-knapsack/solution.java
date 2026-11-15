    static long solve(long n, long cap, long[] w, long[] v, long[] c) {
        long[] dp = new long[(int) cap + 1];
        for (int i = 0; i < n; ++i) {
            long rest = c[i];
            long block = 1;
            while (rest > 0) {
                long take = Math.min(block, rest);
                long bw = w[i] * take;
                long bv = v[i] * take;
                if (bw <= cap) {
                    for (long j = cap; j >= bw; --j) {
                        long cand = dp[(int) (j - bw)] + bv;
                        if (cand > dp[(int) j]) dp[(int) j] = cand;
                    }
                }
                rest -= take;
                block *= 2;
            }
        }
        return dp[(int) cap];
    }
