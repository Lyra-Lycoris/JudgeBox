    static final long MOD = 1000000007L;

    static long[] fibPair(long n) {
        if (n == 0) return new long[]{0, 1};
        long[] prev = fibPair(n >> 1);
        long a = prev[0], b = prev[1];
        long c = a * ((2 * b - a + MOD) % MOD) % MOD;
        long d = (a * a + b * b) % MOD;
        if ((n & 1) == 1) return new long[]{d, (c + d) % MOD};
        return new long[]{c, d};
    }

    static long solve(long n) {
        return fibPair(n)[0];
    }
