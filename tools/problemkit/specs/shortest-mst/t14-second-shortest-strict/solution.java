    static long solve(long n, long m, long[][] e) {
        int nn = (int) n, mm = (int) m;
        int[] head = new int[nn + 1];
        Arrays.fill(head, -1);
        int[] nxt = new int[2 * mm];
        int[] to = new int[2 * mm];
        long[] wt = new long[2 * mm];
        for (int i = 0; i < mm; ++i) {
            int u = (int) e[i][0], v = (int) e[i][1];
            long w = e[i][2];
            to[2 * i] = v; wt[2 * i] = w; nxt[2 * i] = head[u]; head[u] = 2 * i;
            to[2 * i + 1] = u; wt[2 * i + 1] = w; nxt[2 * i + 1] = head[v]; head[v] = 2 * i + 1;
        }
        final long INF = Long.MAX_VALUE / 4;
        long[] d1 = new long[nn + 1];
        long[] d2 = new long[nn + 1];
        Arrays.fill(d1, INF);
        Arrays.fill(d2, INF);
        d1[1] = 0;
        PriorityQueue<long[]> pq = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        pq.add(new long[]{0L, 1L});
        while (!pq.isEmpty()) {
            long[] cur = pq.poll();
            long d = cur[0];
            int u = (int) cur[1];
            if (d > d2[u]) continue;
            for (int i = head[u]; i != -1; i = nxt[i]) {
                int v = to[i];
                long nd = d + wt[i];
                if (nd < d1[v]) {
                    d2[v] = d1[v];
                    d1[v] = nd;
                    pq.add(new long[]{nd, v});
                } else if (nd > d1[v] && nd < d2[v]) {
                    d2[v] = nd;
                    pq.add(new long[]{nd, v});
                }
            }
        }
        return d2[nn] >= INF ? -1L : d2[nn];
    }
