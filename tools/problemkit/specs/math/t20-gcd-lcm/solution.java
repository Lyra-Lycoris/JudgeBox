    static long[] solve(long a, long b) {
        long x = a, y = b;
        while (y != 0) {
            long t = x % y;
            x = y;
            y = t;
        }
        if (x == 0) return new long[]{0, 0};
        return new long[]{x, a / x * b};
    }
