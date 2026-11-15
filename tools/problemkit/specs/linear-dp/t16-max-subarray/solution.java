    static long solve(long n, long[] a) {
        long best = a[0];
        long cur = a[0];
        for (int i = 1; i < n; ++i) {
            long x = a[i];
            cur = (cur > 0 ? cur + x : x);
            if (cur > best) best = cur;
        }
        return best;
    }
