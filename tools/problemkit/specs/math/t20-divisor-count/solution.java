    static long solve(long n) {
        long count = 0;
        for (long d = 1; d * d <= n; ++d) {
            if (n % d == 0) {
                count += (d * d == n) ? 1 : 2;
            }
        }
        return count;
    }
