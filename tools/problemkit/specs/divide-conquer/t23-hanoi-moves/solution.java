    static long solve(long n) {
        long power = 1;
        for (long i = 0; i < n; ++i) power *= 2;
        return power - 1;
    }
