    static long[] solve(long n, long m, long[] r, long[] c) {
        long[] row = new long[(int) n];
        long[] col = new long[(int) m];
        for (int i = 0; i < n; ++i) row[i] = r[i];
        for (int j = 0; j < m; ++j) col[j] = c[j];
        long[] a = new long[(int) (n * m)];
        int at = 0;
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                long x = Math.min(row[i], col[j]);
                a[at++] = x;
                row[i] -= x;
                col[j] -= x;
            }
        }
        return a;
    }
