    static long solve(long n, long[] a) {
        if (n <= 1) return 0;
        PriorityQueue<Long> pq = new PriorityQueue<>();
        for (int i = 0; i < n; ++i) pq.add(a[i]);
        long total = 0;
        while (pq.size() > 1) {
            long x = pq.poll();
            long y = pq.poll();
            total += x + y;
            pq.add(x + y);
        }
        return total;
    }
