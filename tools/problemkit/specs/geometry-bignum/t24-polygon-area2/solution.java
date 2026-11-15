    static long solve(long n, long[] xs, long[] ys) {
        long total = 0;
        long px = xs[(int) (n - 1)];
        long py = ys[(int) (n - 1)];
        for (int i = 0; i < (int) n; ++i) {
            long cx = xs[i];
            long cy = ys[i];
            total += px * cy - cx * py;
            px = cx;
            py = cy;
        }
        return total < 0 ? -total : total;
    }
