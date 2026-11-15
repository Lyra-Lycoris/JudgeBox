    static long solve(long n, long[] a) {
        long notTake = 0;
        long take = a[0];
        for (int i = 1; i < n; ++i) {
            long newTake = notTake + a[i];
            long newNot = Math.max(notTake, take);
            notTake = newNot;
            take = newTake;
        }
        return Math.max(notTake, take);
    }
