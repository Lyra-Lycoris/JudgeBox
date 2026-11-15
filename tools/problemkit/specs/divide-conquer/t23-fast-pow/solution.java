    static long powMod(long base, long exp, long mod) {
        if (exp == 0) return 1 % mod;
        long half = powMod(base, exp / 2, mod);
        long result = half * half % mod;
        if ((exp & 1) == 1) result = result * (base % mod) % mod;
        return result;
    }

    static long solve(long a, long b, long m) {
        return powMod(a % m, b, m);
    }
