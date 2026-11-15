    static long solve(long n, long x, long y, long p, long q) {
        final long MOD = 1000000007L;
        if (n == 0) return x % MOD;
        if (n == 1) return y % MOD;
        long m00 = p % MOD, m01 = q % MOD, m10 = 1, m11 = 0;
        long r00 = 1, r01 = 0, r10 = 0, r11 = 1;
        long e = n - 1;
        while (e > 0) {
            if ((e & 1L) != 0) {
                long t00 = (r00 * m00 + r01 * m10) % MOD;
                long t01 = (r00 * m01 + r01 * m11) % MOD;
                long t10 = (r10 * m00 + r11 * m10) % MOD;
                long t11 = (r10 * m01 + r11 * m11) % MOD;
                r00 = t00;
                r01 = t01;
                r10 = t10;
                r11 = t11;
            }
            long s00 = (m00 * m00 + m01 * m10) % MOD;
            long s01 = (m00 * m01 + m01 * m11) % MOD;
            long s10 = (m10 * m00 + m11 * m10) % MOD;
            long s11 = (m10 * m01 + m11 * m11) % MOD;
            m00 = s00;
            m01 = s01;
            m10 = s10;
            m11 = s11;
            e >>= 1;
        }
        return (r00 * y + r01 * x) % MOD;
    }
