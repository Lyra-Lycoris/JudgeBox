    static long[] solve(long n, long[] a) {
        long x = 0;
        for (long v : a) x ^= v;
        long lowbit = x & (-x);
        long p = 0, q = 0;
        for (long v : a) {
            if ((v & lowbit) != 0) p ^= v;
            else q ^= v;
        }
        if (p < q) return new long[] {p, q};
        return new long[] {q, p};
    }
