    static long solve(long n, long[] a, long k) {
        long lo = 0, hi = 0;
        for (long x : a) {
            lo = Math.max(lo, x);
            hi += x;
        }
        while (lo < hi) {
            long mid = lo + (hi - lo) / 2;
            long parts = 1, cur = 0;
            for (long x : a) {
                if (cur + x > mid) {
                    ++parts;
                    cur = x;
                    if (parts > k) break;
                } else {
                    cur += x;
                }
            }
            if (parts <= k) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
