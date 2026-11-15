    static long solve(long n, long[] a) {
        long lo = 0, hi = n - 1;
        while (lo < hi) {
            long mid = lo + (hi - lo) / 2;
            if (a[(int) mid] > a[(int) hi]) lo = mid + 1;
            else hi = mid;
        }
        return a[(int) lo];
    }
