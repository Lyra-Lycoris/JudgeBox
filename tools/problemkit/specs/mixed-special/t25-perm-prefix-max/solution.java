    static long[] solve(long n, long k) {
        int size = (int) n;
        long[] p = new long[size];
        int at = 0;
        for (long x = 1; x <= k - 1; ++x) p[at++] = x;
        for (long x = n; x >= k; --x) p[at++] = x;
        return p;
    }
