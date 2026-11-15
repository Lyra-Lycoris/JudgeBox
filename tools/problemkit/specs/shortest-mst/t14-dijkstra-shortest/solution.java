    static long[] solve(long n, long m, long s, long[][] e) {
        int nn = (int) n, mm = (int) m;
        int[] head = new int[nn + 1];
        Arrays.fill(head, -1);
        int[] nxt = new int[mm];
        int[] to = new int[mm];
        long[] wt = new long[mm];
        for (int i = 0; i < mm; ++i) {
            int u = (int) e[i][0];
            to[i] = (int) e[i][1];
            wt[i] = e[i][2];
            nxt[i] = head[u];
            head[u] = i;
        }
        final long INF = Long.MAX_VALUE / 4;
        long[] dist = new long[nn + 1];
        Arrays.fill(dist, INF);
        dist[(int) s] = 0;
        PriorityQueue<long[]> pq = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        pq.add(new long[]{0L, s});
        while (!pq.isEmpty()) {
            long[] cur = pq.poll();
            long d = cur[0];
            int u = (int) cur[1];
            if (d != dist[u]) continue;
            for (int i = head[u]; i != -1; i = nxt[i]) {
                int v = to[i];
                long nd = d + wt[i];
                if (nd < dist[v]) {
                    dist[v] = nd;
                    pq.add(new long[]{nd, v});
                }
            }
        }
        long[] answer = new long[nn];
        for (int i = 1; i <= nn; ++i) answer[i - 1] = dist[i] >= INF ? -1L : dist[i];
        return answer;
    }
