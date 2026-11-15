    static long solve(long n, long[] a, long x) {
        long lo = 0, hi = n;
        while (lo < hi) {
            long mid = lo + (hi - lo) / 2;
            if (a[(int) mid] >= x) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
