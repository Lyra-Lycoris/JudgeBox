    static long[] solve(long n, long[][] w) {
        int nn = (int) n;
        final long INF = Long.MAX_VALUE / 4;
        long[][] d = new long[nn][nn];
        for (int i = 0; i < nn; ++i) {
            for (int j = 0; j < nn; ++j) d[i][j] = w[i][j] < 0 ? INF : w[i][j];
            d[i][i] = 0;
        }
        for (int k = 0; k < nn; ++k) {
            long[] dk = d[k];
            for (int i = 0; i < nn; ++i) {
                long dik = d[i][k];
                if (dik >= INF) continue;
                long[] di = d[i];
                for (int j = 0; j < nn; ++j) {
                    long nd = dik + dk[j];
                    if (nd < di[j]) di[j] = nd;
                }
            }
        }
        long[] answer = new long[nn * nn];
        for (int i = 0; i < nn; ++i) {
            for (int j = 0; j < nn; ++j) {
                long x = d[i][j];
                answer[i * nn + j] = x >= INF ? -1L : x;
            }
        }
        return answer;
    }
