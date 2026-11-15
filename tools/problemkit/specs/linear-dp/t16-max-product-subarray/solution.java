    static long solve(long n, long[] a) {
        long best = a[0];
        long mx = a[0];
        long mn = a[0];
        for (int i = 1; i < n; ++i) {
            long x = a[i];
            long c1 = mx * x;
            long c2 = mn * x;
            long newMax = Math.max(x, Math.max(c1, c2));
            long newMin = Math.min(x, Math.min(c1, c2));
            mx = newMax;
            mn = newMin;
            if (mx > best) best = mx;
        }
        return best;
    }
