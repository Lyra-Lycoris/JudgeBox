    static long solve(long n, long[] l, long[] r) {
        final long SHIFT = 1000000000L;
        final long BASE = 2000000001L;
        long[] keys = new long[(int) n];
        for (int i = 0; i < n; ++i) keys[i] = (r[i] + SHIFT) * BASE + (l[i] + SHIFT);
        Arrays.sort(keys);
        long answer = 0;
        long lastEnd = -(1L << 60);
        for (int i = 0; i < n; ++i) {
            long li = keys[i] % BASE - SHIFT;
            long ri = keys[i] / BASE - SHIFT;
            if (li >= lastEnd) {
                ++answer;
                lastEnd = ri;
            }
        }
        return answer;
    }
