    static long solve(long n, long[] s, long[] e) {
        long[] ss = s.clone();
        long[] ee = e.clone();
        Arrays.sort(ss);
        Arrays.sort(ee);
        long i = 0, j = 0, cur = 0, best = 0;
        while (i < n) {
            if (ss[(int) i] < ee[(int) j]) {
                ++cur;
                if (cur > best) best = cur;
                ++i;
            } else {
                --cur;
                ++j;
            }
        }
        return best;
    }
