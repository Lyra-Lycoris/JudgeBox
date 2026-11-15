    static long solve(long n, long[] a, long k) {
        if (k <= 1) return 0;
        long[] b = a.clone();
        Arrays.sort(b);
        long lo = 0, hi = (b[(int) n - 1] - b[0]) / (k - 1);
        while (lo < hi) {
            long mid = (lo + hi + 1) / 2;
            long cnt = 1, last = b[0];
            for (int i = 1; i < n; ++i) {
                if (b[i] - last >= mid) {
                    ++cnt;
                    last = b[i];
                    if (cnt >= k) break;
                }
            }
            if (cnt >= k) lo = mid;
            else hi = mid - 1;
        }
        return lo;
    }
