    static long solve(long n, long k, long[] arrive, long[] serve) {
        PriorityQueue<Long> freeAt = new PriorityQueue<>();
        for (long i = 0; i < k; ++i) freeAt.add(0L);
        long total = 0;
        for (int i = 0; i < n; ++i) {
            long free = freeAt.poll();
            long start = Math.max(free, arrive[i]);
            total += start - arrive[i];
            freeAt.add(start + serve[i]);
        }
        return total;
    }
