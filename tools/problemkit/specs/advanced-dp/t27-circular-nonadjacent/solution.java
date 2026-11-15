    static long solve(long n, long[] a) {
        int N = (int) n;
        if (N == 1) return a[0] > 0 ? a[0] : 0;
        long p2 = 0, p1 = 0;
        for (int i = 0; i <= N - 2; ++i) {
            long cur = p2 + a[i];
            if (p1 > cur) cur = p1;
            p2 = p1;
            p1 = cur;
        }
        long r1 = p1;
        p2 = 0;
        p1 = 0;
        for (int i = 1; i <= N - 1; ++i) {
            long cur = p2 + a[i];
            if (p1 > cur) cur = p1;
            p2 = p1;
            p1 = cur;
        }
        long r2 = p1;
        return r1 > r2 ? r1 : r2;
    }
