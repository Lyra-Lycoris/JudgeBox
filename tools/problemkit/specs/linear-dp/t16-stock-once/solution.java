    static long solve(long n, long[] a) {
        long best = 0;
        long mn = a[0];
        for (int i = 1; i < n; ++i) {
            long profit = a[i] - mn;
            if (profit > best) best = profit;
            if (a[i] < mn) mn = a[i];
        }
        return best;
    }
