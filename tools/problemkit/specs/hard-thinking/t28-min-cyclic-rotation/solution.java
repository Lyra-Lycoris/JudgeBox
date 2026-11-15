    static long[] solve(long n, long[] a) {
        long i = 0, j = 1, k = 0;
        int len = (int) n;
        while (i < n && j < n && k < n) {
            long x = a[(int) ((i + k) % n)];
            long y = a[(int) ((j + k) % n)];
            if (x == y) {
                ++k;
            } else if (x > y) {
                i = i + k + 1;
                if (i == j) ++i;
                k = 0;
            } else {
                j = j + k + 1;
                if (i == j) ++j;
                k = 0;
            }
        }
        int start = (int) Math.min(i, j);
        if (start >= len) start = 0;
        long[] result = new long[len];
        for (int t = 0; t < len; ++t) result[t] = a[(start + t) % len];
        return result;
    }
