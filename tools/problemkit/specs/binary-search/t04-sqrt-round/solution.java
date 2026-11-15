    static long solve(long x) {
        long lo = 0, hi = 1000000001L;
        while (lo + 1 < hi) {
            long mid = lo + (hi - lo) / 2;
            long t = 2 * mid - 1;
            if (t * t <= 4 * x * 1000000L) lo = mid;
            else hi = mid;
        }
        return lo;
    }
