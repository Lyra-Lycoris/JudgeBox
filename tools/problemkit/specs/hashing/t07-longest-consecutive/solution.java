    static long solve(long n, long[] a) {
        Set<Long> present = new HashSet<>();
        for (long x : a) present.add(x);
        long best = 0;
        for (long x : a) {
            if (present.contains(x - 1)) continue;
            long y = x;
            while (present.contains(y + 1)) ++y;
            best = Math.max(best, y - x + 1);
        }
        return best;
    }
