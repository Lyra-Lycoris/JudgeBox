    static long modPow(long base, long exp, long mod) {
        long result = 1 % mod;
        base %= mod;
        while (exp > 0) {
            if ((exp & 1) == 1) result = result * base % mod;
            base = base * base % mod;
            exp >>= 1;
        }
        return result;
    }

    static long solve(long n, long k, long p) {
        if (k < 0 || k > n) return 0;
        if (k > n - k) k = n - k;
        long numerator = 1;
        long denominator = 1;
        for (long i = 1; i <= k; ++i) {
            numerator = numerator * ((n - k + i) % p) % p;
            denominator = denominator * (i % p) % p;
        }
        return numerator * modPow(denominator, p - 2, p) % p;
    }
