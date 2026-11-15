    static boolean solve(long target, long n, long[] a) {
        long[] sums = new long[1 << a.length];
        int size = 1;
        for (long x : a) {
            for (int i = 0; i < size; ++i) sums[size + i] = sums[i] + x;
            size *= 2;
        }
        for (int i = 0; i < size; ++i) if (sums[i] == target) return true;
        return false;
    }
