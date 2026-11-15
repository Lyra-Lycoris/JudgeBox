    static long solve(long n, long[] g, long m, long[] s) {
        long[] gg = g.clone();
        long[] ss = s.clone();
        Arrays.sort(gg);
        Arrays.sort(ss);
        long i = 0, j = 0;
        while (i < n && j < m) {
            if (ss[(int) j] >= gg[(int) i]) ++i;
            ++j;
        }
        return i;
    }
