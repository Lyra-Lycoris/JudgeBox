    static long solve(long n, long[] a) {
        long candidate = a[0];
        long balance = 0;
        for (long x : a) {
            if (balance == 0) candidate = x;
            balance += (x == candidate) ? 1 : -1;
        }
        return candidate;
    }
