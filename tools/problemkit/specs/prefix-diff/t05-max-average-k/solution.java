    static long solve(long n, long k, long[] a) {
        int size = (int) n;
        long[] pre = new long[size + 1];
        for (int i = 0; i < size; ++i) pre[i + 1] = pre[i] + a[i];
        long lo = -1000000000001L, hi = 1000000000000L;
        while (lo + 1 < hi) {
            long mid = lo + (hi - lo) / 2;
            long best = 0;
            boolean feasible = false;
            for (long j = k; j <= n; ++j) {
                long i = j - k;
                long candidate = pre[(int) i] * 1000 - mid * i;
                if (candidate < best) best = candidate;
                if (pre[(int) j] * 1000 - mid * j >= best) {
                    feasible = true;
                    break;
                }
            }
            if (feasible) {
                lo = mid;
            } else {
                hi = mid;
            }
        }
        return lo;
    }
