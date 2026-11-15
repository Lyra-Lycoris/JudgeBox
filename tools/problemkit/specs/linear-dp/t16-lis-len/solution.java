    static long solve(long n, long[] a) {
        long[] tails = new long[(int) n];
        int len = 0;
        for (int i = 0; i < n; ++i) {
            long x = a[i];
            int lo = 0, hi = len;
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (tails[mid] < x) lo = mid + 1;
                else hi = mid;
            }
            tails[lo] = x;
            if (lo == len) ++len;
        }
        return len;
    }
