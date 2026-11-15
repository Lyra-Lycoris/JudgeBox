    static long kth(long[] a, long[] b, long k) {
        int na = a.length, nb = b.length;
        int i = 0, j = 0;
        while (true) {
            if (i == na) return b[j + (int) k];
            if (j == nb) return a[i + (int) k];
            if (k == 0) return Math.min(a[i], b[j]);
            long step = (k + 1) / 2;
            int ai = i + (int) Math.min(na - i, step) - 1;
            int bj = j + (int) Math.min(nb - j, step) - 1;
            if (a[ai] <= b[bj]) {
                k -= ai - i + 1;
                i = ai + 1;
            } else {
                k -= bj - j + 1;
                j = bj + 1;
            }
        }
    }

    static long solve(long n, long[] a, long m, long[] b) {
        long total = n + m;
        return kth(a, b, (total - 1) / 2) + kth(a, b, total / 2);
    }
