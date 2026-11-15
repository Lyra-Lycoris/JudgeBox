    static long gray(long n, long k) {
        if (n == 0) return 0;
        long half = 1L << (n - 1);
        if (k < half) return gray(n - 1, k);
        return half + gray(n - 1, 2 * half - 1 - k);
    }

    static long solve(long n, long k) {
        return gray(n, k);
    }
