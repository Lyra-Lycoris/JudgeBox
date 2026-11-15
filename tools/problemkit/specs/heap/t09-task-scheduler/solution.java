    static long solve(long n, long c, long[] tasks) {
        HashMap<Long, Long> count = new HashMap<Long, Long>();
        for (long x : tasks) {
            Long cur = count.get(x);
            count.put(x, cur == null ? 1L : cur + 1);
        }
        PriorityQueue<Long> heap = new PriorityQueue<Long>(Collections.reverseOrder());
        for (long v : count.values()) heap.add(v);
        long time = 0;
        while (!heap.isEmpty()) {
            long slot = Math.min(c + 1, (long) heap.size());
            ArrayList<Long> rest = new ArrayList<Long>();
            for (long i = 0; i < slot; ++i) {
                long top = heap.poll();
                if (top > 1) rest.add(top - 1);
            }
            time += c + 1;
            for (long v : rest) heap.add(v);
            if (heap.isEmpty()) time -= c + 1 - slot;
        }
        return time;
    }
