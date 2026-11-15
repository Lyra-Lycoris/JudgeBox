    static long solve(long n, long[][] seg) {
        int sz = (int) n;
        long[][] a = new long[sz][];
        for (int i = 0; i < sz; ++i) {
            a[i] = new long[] {seg[i][1], seg[i][0], seg[i][2]};
        }
        Arrays.sort(a, new Comparator<long[]>() {
            public int compare(long[] x, long[] y) {
                if (x[0] != y[0]) return Long.compare(x[0], y[0]);
                if (x[1] != y[1]) return Long.compare(x[1], y[1]);
                return Long.compare(x[2], y[2]);
            }
        });
        long[] ends = new long[sz];
        for (int i = 0; i < sz; ++i) ends[i] = a[i][0];
        long[] dp = new long[sz + 1];
        for (int i = 0; i < sz; ++i) {
            long l = a[i][1];
            long w = a[i][2];
            int lo = 0, hi = sz;
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (ends[mid] < l) lo = mid + 1;
                else hi = mid;
            }
            long best = dp[lo] + w;
            dp[i + 1] = Math.max(dp[i], best);
        }
        return dp[sz];
    }
