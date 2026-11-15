    static long[] solve(long n) {
        long[] a = new long[(int) n];
        for (int i = 0; i < a.length; ++i) a[i] = (i % 2 == 0) ? 1 : 2;
        return a;
    }
