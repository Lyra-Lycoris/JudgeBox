    static long solve(long n, long[] a) {
        long best = 0;
        for (int i = 0; i < n; ++i) {
            long ai = a[i];
            for (int j = i + 1; j < n; ++j) {
                long v = ai ^ a[j];
                if (v > best) best = v;
            }
        }
        return best;
    }
