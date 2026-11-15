    static long solve(long n, long m, long[] s, long[] d) {
        long[][] meetings = new long[(int) m][2];
        for (int i = 0; i < (int) m; ++i) {
            meetings[i][0] = s[i];
            meetings[i][1] = i;
        }
        Arrays.sort(meetings, new Comparator<long[]>() {
            public int compare(long[] x, long[] y) {
                if (x[0] != y[0]) return Long.compare(x[0], y[0]);
                return Long.compare(x[1], y[1]);
            }
        });
        long[] used = new long[(int) n];
        PriorityQueue<Long> free = new PriorityQueue<Long>();
        for (long i = 0; i < n; ++i) free.add(i);
        PriorityQueue<long[]> busy = new PriorityQueue<long[]>(new Comparator<long[]>() {
            public int compare(long[] x, long[] y) {
                if (x[0] != y[0]) return Long.compare(x[0], y[0]);
                return Long.compare(x[1], y[1]);
            }
        });
        for (int p = 0; p < (int) m; ++p) {
            int idx = (int) meetings[p][1];
            long start = meetings[p][0];
            while (!busy.isEmpty() && busy.peek()[0] <= start) {
                long[] cur = busy.poll();
                free.add(cur[1]);
            }
            long room;
            if (!free.isEmpty()) {
                room = free.poll();
                busy.add(new long[] {start + d[idx], room});
            } else {
                long[] cur = busy.poll();
                room = cur[1];
                busy.add(new long[] {cur[0] + d[idx], room});
            }
            used[(int) room] += 1;
        }
        long best = 0;
        for (long i = 1; i < n; ++i) {
            if (used[(int) i] > used[(int) best]) best = i;
        }
        return best;
    }
