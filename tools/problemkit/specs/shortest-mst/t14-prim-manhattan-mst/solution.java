    static long solve(long n, long[][] p) {
        int nn = (int) n;
        final long INF = Long.MAX_VALUE / 4;
        long[] best = new long[nn];
        Arrays.fill(best, INF);
        boolean[] used = new boolean[nn];
        best[0] = 0;
        long total = 0;
        for (int round = 0; round < nn; ++round) {
            int u = -1;
            long bd = INF;
            for (int i = 0; i < nn; ++i) {
                if (!used[i] && best[i] < bd) {
                    bd = best[i];
                    u = i;
                }
            }
            used[u] = true;
            total += bd;
            long xu = p[u][0], yu = p[u][1];
            for (int i = 0; i < nn; ++i) {
                if (used[i]) continue;
                long d = Math.abs(p[i][0] - xu) + Math.abs(p[i][1] - yu);
                if (d < best[i]) best[i] = d;
            }
        }
        return total;
    }
