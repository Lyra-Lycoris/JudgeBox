    static long solve(long n) {
        long result = n;
        long x = n;
        for (long p = 2; p * p <= x; ++p) {
            if (x % p == 0) {
                while (x % p == 0) x /= p;
                result -= result / p;
            }
        }
        if (x > 1) result -= result / x;
        return result;
    }
