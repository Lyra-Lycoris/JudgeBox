    static long solve(long n, long[] l, long[] r, long m) {
        final long SHIFT = 1000000000L;
        final long BASE = 2000000001L;
        long[] keys = new long[(int) n];
        for (int i = 0; i < n; ++i) keys[i] = (l[i] + SHIFT) * BASE + (r[i] + SHIFT);
        Arrays.sort(keys);
        long i = 0, cur = 0, count = 0;
        while (cur < m) {
            long best = -1;
            while (i < n && keys[(int) i] / BASE - SHIFT <= cur) {
                long rr = keys[(int) i] % BASE - SHIFT;
                if (rr > best) best = rr;
                ++i;
            }
            if (best <= cur) return -1;
            cur = best;
            ++count;
        }
        return count;
    }
