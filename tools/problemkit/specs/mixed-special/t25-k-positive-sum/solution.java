    static long[] solve(long s, long k) {
        long[] v = new long[(int) k];
        for (int i = 0; i < k - 1; ++i) v[i] = 1;
        v[(int) (k - 1)] = s - (k - 1);
        return v;
    }
