    static long solve(long n, long[] a, long l, long r) {
        int size = (int) n;
        long[] pre = new long[size + 1];
        for (int i = 0; i < size; ++i) pre[i + 1] = pre[i] + a[i];
        return pre[(int) r] - pre[(int) l - 1];
    }
