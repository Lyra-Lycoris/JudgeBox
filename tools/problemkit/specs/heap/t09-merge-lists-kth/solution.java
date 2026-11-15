    static long solve(long k, long m, long t, long[][] lists) {
        PriorityQueue<long[]> heap = new PriorityQueue<long[]>(new Comparator<long[]>() {
            public int compare(long[] x, long[] y) {
                if (x[0] != y[0]) return Long.compare(x[0], y[0]);
                if (x[1] != y[1]) return Long.compare(x[1], y[1]);
                return Long.compare(x[2], y[2]);
            }
        });
        for (int r = 0; r < (int) k; ++r) heap.add(new long[] {lists[r][0], r, 0});
        long answer = 0;
        for (long step = 0; step < t; ++step) {
            long[] cur = heap.poll();
            answer = cur[0];
            int r = (int) cur[1];
            int c = (int) cur[2];
            if (c + 1 < (int) m) heap.add(new long[] {lists[r][c + 1], r, c + 1});
        }
        return answer;
    }
