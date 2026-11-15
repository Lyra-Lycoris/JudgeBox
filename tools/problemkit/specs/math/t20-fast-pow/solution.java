    static long solve(long a, long b, long m) {
        if (m == 1) return 0;
        long result = 1 % m;
        a %= m;
        while (b > 0) {
            if ((b & 1) == 1) result = result * a % m;
            a = a * a % m;
            b >>= 1;
        }
        return result;
    }
