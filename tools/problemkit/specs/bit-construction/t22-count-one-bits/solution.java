    static long solve(long n) {
        long count = 0;
        while (n > 0) {
            n &= n - 1;
            ++count;
        }
        return count;
    }
