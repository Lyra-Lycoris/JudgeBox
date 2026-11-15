    static long solve(long n, long[] a) {
        final long MOD = 1000000007L;
        long mask = 0;
        for (long v : a) mask |= v;
        long base = 2;
        long exponent = n - 1;
        long power = 1;
        while (exponent > 0) {
            if ((exponent & 1L) != 0) power = power * base % MOD;
            base = base * base % MOD;
            exponent >>= 1;
        }
        return mask % MOD * power % MOD;
    }
