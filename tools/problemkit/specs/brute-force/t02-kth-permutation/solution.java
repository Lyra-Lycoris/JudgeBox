    static long[] solve(long n, long k) {
        int len = (int) n;
        long[] p = new long[len];
        for (int i = 0; i < len; ++i) p[i] = i + 1;
        for (long step = 1; step < k; ++step) {
            int i = len - 2;
            while (i >= 0 && p[i] >= p[i + 1]) --i;
            if (i < 0) break;
            int j = len - 1;
            while (p[j] <= p[i]) --j;
            long t = p[i];
            p[i] = p[j];
            p[j] = t;
            int l = i + 1, r = len - 1;
            while (l < r) {
                long tmp = p[l];
                p[l] = p[r];
                p[r] = tmp;
                ++l;
                --r;
            }
        }
        return p;
    }
