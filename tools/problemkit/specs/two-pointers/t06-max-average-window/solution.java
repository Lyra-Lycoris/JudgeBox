    static long absLong(long x) {
        return x < 0 ? -x : x;
    }

    static long gcdLong(long x, long y) {
        x = absLong(x);
        y = absLong(y);
        while (y != 0) {
            long t = x % y;
            x = y;
            y = t;
        }
        return x;
    }

    static String solve(long n, long k, long[] a) {
        long cur = 0;
        int len = (int) k;
        for (int i = 0; i < len; ++i) cur += a[i];
        long best = cur;
        for (int i = len; i < (int) n; ++i) {
            cur += a[i] - a[i - len];
            if (cur > best) best = cur;
        }
        long g = gcdLong(best, k);
        long p = best / g;
        long q = k / g;
        if (q < 0) {
            p = -p;
            q = -q;
        }
        return p + "/" + q;
    }
