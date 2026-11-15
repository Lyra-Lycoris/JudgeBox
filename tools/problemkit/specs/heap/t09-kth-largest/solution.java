    static long solve(long n, long k, long[] a) {
        PriorityQueue<Long> heap = new PriorityQueue<Long>();
        for (long x : a) {
            heap.add(x);
            if (heap.size() > k) heap.poll();
        }
        return heap.peek();
    }
