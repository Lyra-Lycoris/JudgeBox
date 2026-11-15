    static long turn(long[] o, long[] a, long[] b) {
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
    }

    static long solve(long n, long[] xs, long[] ys) {
        int cnt = (int) n;
        long[][] pts = new long[cnt][2];
        for (int i = 0; i < cnt; ++i) {
            pts[i][0] = xs[i];
            pts[i][1] = ys[i];
        }
        Arrays.sort(pts, (p, q) -> p[0] != q[0] ? Long.compare(p[0], q[0]) : Long.compare(p[1], q[1]));
        int m = 0;
        for (int i = 0; i < cnt; ++i) {
            if (i == 0 || pts[i][0] != pts[m - 1][0] || pts[i][1] != pts[m - 1][1]) {
                pts[m][0] = pts[i][0];
                pts[m][1] = pts[i][1];
                ++m;
            }
        }
        if (m <= 2) {
            return m;
        }
        int[] lower = new int[m + 1];
        int ls = 0;
        for (int i = 0; i < m; ++i) {
            while (ls >= 2 && turn(pts[lower[ls - 2]], pts[lower[ls - 1]], pts[i]) <= 0) {
                --ls;
            }
            lower[ls++] = i;
        }
        int[] upper = new int[m + 1];
        int us = 0;
        for (int i = m - 1; i >= 0; --i) {
            while (us >= 2 && turn(pts[upper[us - 2]], pts[upper[us - 1]], pts[i]) <= 0) {
                --us;
            }
            upper[us++] = i;
        }
        return (long) ls + (long) us - 2;
    }
