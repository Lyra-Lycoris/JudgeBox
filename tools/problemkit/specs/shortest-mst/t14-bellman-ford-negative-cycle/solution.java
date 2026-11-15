    static boolean solve(long n, long m, long s, long[][] e) {
        int nn = (int) n, mm = (int) m;
        final long INF = Long.MAX_VALUE / 4;
        long[] dist = new long[nn + 1];
        Arrays.fill(dist, INF);
        dist[(int) s] = 0;
        for (int round = 0; round < nn; ++round) {
            boolean changed = false;
            for (int i = 0; i < mm; ++i) {
                int u = (int) e[i][0];
                int v = (int) e[i][1];
                long w = e[i][2];
                if (dist[u] >= INF) continue;
                long nd = dist[u] + w;
                if (nd < dist[v]) {
                    dist[v] = nd;
                    changed = true;
                }
            }
            if (!changed) return false;
        }
        return true;
    }
