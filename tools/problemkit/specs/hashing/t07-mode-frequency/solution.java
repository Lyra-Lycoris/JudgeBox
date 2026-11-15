    static long solve(long n, long[] a) {
        Map<Long, Integer> counts = new HashMap<>();
        long best = 0;
        for (long x : a) {
            int current = counts.getOrDefault(x, 0) + 1;
            counts.put(x, current);
            if (current > best) best = current;
        }
        return best;
    }
