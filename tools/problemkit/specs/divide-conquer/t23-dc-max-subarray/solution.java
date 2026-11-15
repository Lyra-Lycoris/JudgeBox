    static long solve(long n, long[] a) {
        long best = a[0];
        long current = a[0];
        for (int i = 1; i < (int) n; ++i) {
            current = (current > 0 ? current + a[i] : a[i]);
            if (current > best) best = current;
        }
        return best;
    }
