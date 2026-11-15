    static long solve(long n, long[] a) {
        if (n <= 1) return 0;
        PriorityQueue<Long> heap = new PriorityQueue<Long>();
        long total = 0;
        for (long x : a) {
            heap.add(x);
            total += x;
        }
        long cost = 0;
        while (heap.size() > 1) {
            long x = heap.poll();
            long y = heap.poll();
            cost += x + y;
            heap.add(x + y);
        }
        return cost - total;
    }
