    static long solve(long n, long k, long[] a) {
        long total = 0;
        for (long x : a) total += x;
        long lo = 0, hi = total / k;
        while (lo < hi) {
            long mid = (lo + hi + 1) / 2;
            long cnt = 0, cur = 0;
            for (long x : a) {
                cur += x;
                if (cur >= mid) {
                    ++cnt;
                    cur = 0;
                    if (cnt >= k) break;
                }
            }
            if (cnt >= k) {
                lo = mid;
            } else {
                hi = mid - 1;
            }
        }
        return lo;
    }
