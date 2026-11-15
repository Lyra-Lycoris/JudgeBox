    static long solve(long n, long[] a) {
        long lo = 0, hi = n - 1;
        while (lo < hi) {
            long mid = lo + (hi - lo) / 2;
            if (a[(int) mid] < a[(int) mid + 1]) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }
