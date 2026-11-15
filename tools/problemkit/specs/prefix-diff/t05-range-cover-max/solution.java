    static long[] solve(long n, long q, long[][] segs) {
        int size = (int) n;
        long[] diff = new long[size + 1];
        for (int i = 0; i < (int) q; ++i) {
            int l = (int) segs[i][0];
            int r = (int) segs[i][1];
            diff[l - 1] += 1;
            diff[r] -= 1;
        }
        long cur = 0, best = -1, bestPos = 1;
        for (int i = 0; i < size; ++i) {
            cur += diff[i];
            if (cur > best) {
                best = cur;
                bestPos = i + 1;
            }
        }
        return new long[] {best, bestPos};
    }
