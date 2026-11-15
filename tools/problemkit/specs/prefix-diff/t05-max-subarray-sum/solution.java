    static long solve(long n, long[] a) {
        long best = a[0];
        long prefix = 0;
        long minPrefix = 0;
        for (int i = 0; i < (int) n; ++i) {
            prefix += a[i];
            long candidate = prefix - minPrefix;
            if (candidate > best) best = candidate;
            if (prefix < minPrefix) minPrefix = prefix;
        }
        return best;
    }
