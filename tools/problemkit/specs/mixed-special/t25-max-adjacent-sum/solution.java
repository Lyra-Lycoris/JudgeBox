    static long[] solve(long n) {
        long[] p = new long[(int) n];
        int at = 0;
        p[at++] = (n + 1) / 2;
        long hi = n, lo = 1;
        while (at < n) {
            p[at++] = hi--;
            if (at < n) p[at++] = lo++;
        }
        return p;
    }
