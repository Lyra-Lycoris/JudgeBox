    static long[] solve(long n, long m, long[][] g, long q, long[][] queries) {
        int rows = (int) n, cols = (int) m;
        long[][] pre = new long[rows + 1][cols + 1];
        for (int i = 1; i <= rows; ++i) {
            long running = 0;
            for (int j = 1; j <= cols; ++j) {
                running += g[i - 1][j - 1];
                pre[i][j] = pre[i - 1][j] + running;
            }
        }
        long[] answer = new long[(int) q];
        for (int t = 0; t < (int) q; ++t) {
            int x1 = (int) queries[t][0], y1 = (int) queries[t][1];
            int x2 = (int) queries[t][2], y2 = (int) queries[t][3];
            answer[t] = pre[x2][y2] - pre[x1 - 1][y2] - pre[x2][y1 - 1] + pre[x1 - 1][y1 - 1];
        }
        return answer;
    }
