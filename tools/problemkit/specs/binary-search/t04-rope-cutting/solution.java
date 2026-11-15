    static long solve(long n, long[] a, long k) {
        long lo = 0, hi = 0;
        for (long x : a) hi = Math.max(hi, x);
        while (lo < hi) {
            long mid = lo + (hi - lo + 1) / 2;
            long cnt = 0;
            for (long x : a) {
                cnt += x / mid;
                if (cnt >= k) break;
            }
            if (cnt >= k) lo = mid;
            else hi = mid - 1;
        }
        return lo;
    }
