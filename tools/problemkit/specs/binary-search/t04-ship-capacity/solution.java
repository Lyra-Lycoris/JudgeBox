    static long solve(long n, long[] w, long d) {
        long lo = 0, hi = 0;
        for (long x : w) {
            lo = Math.max(lo, x);
            hi += x;
        }
        while (lo < hi) {
            long mid = lo + (hi - lo) / 2;
            long days = 1, cur = 0;
            for (long x : w) {
                if (cur + x > mid) {
                    ++days;
                    cur = x;
                    if (days > d) break;
                } else {
                    cur += x;
                }
            }
            if (days <= d) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
