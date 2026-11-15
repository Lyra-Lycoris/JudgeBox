    static long[] solve(long n, long m, long k, long[] a, long[] b) {
        PriorityQueue<long[]> heap = new PriorityQueue<long[]>(new Comparator<long[]>() {
            public int compare(long[] x, long[] y) {
                if (x[0] != y[0]) return Long.compare(x[0], y[0]);
                if (x[1] != y[1]) return Long.compare(x[1], y[1]);
                return Long.compare(x[2], y[2]);
            }
        });
        heap.add(new long[] {a[0] + b[0], 0, 0});
        long[] answer = new long[(int) k];
        int filled = 0;
        while (filled < (int) k) {
            long[] cur = heap.poll();
            answer[filled] = cur[0];
            filled++;
            int i = (int) cur[1];
            int j = (int) cur[2];
            if (i + 1 < (int) n) heap.add(new long[] {a[i + 1] + b[j], i + 1, j});
            if (i == 0 && j + 1 < (int) m) heap.add(new long[] {a[i] + b[j + 1], i, j + 1});
        }
        return answer;
    }
