    static long solve(long n, long[] a, long m, long[] b, long x) {
        long[] c = b.clone();
        Arrays.sort(c);
        long ans = 0;
        for (long v : a) {
            long need = x - v;
            int lo = 0, hi = c.length;
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (c[mid] <= need) lo = mid + 1;
                else hi = mid;
            }
            ans += lo;
        }
        return ans;
    }
