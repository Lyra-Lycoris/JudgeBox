    static boolean solve(long n, long[] a) {
        long x = 0;
        boolean allOne = true;
        for (long v : a) {
            x ^= v;
            if (v != 1) allOne = false;
        }
        if (allOne) return n % 2 == 0;
        return x != 0;
    }
