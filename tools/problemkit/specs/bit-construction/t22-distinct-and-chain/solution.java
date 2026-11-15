    static long[] solve(long n) {
        final int SHIFT = 40;
        long[] a = new long[(int) n];
        long value = 1;
        for (int i = 0; i < a.length; ++i) {
            if (i % 2 == 0) {
                a[i] = value;
            } else {
                a[i] = value << SHIFT;
                ++value;
            }
        }
        return a;
    }
