    static long solve(long n, long m, long[][] grid) {
        int N = (int) n;
        int M = (int) m;
        int total = N * M;
        int[] dist = new int[total];
        Arrays.fill(dist, -1);
        int[] queue = new int[total];
        int head = 0, tail = 0;
        long fresh = 0;
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < M; ++j) {
                if (grid[i][j] == 2) {
                    dist[i * M + j] = 0;
                    queue[tail++] = i * M + j;
                } else if (grid[i][j] == 1) {
                    ++fresh;
                }
            }
        }
        if (fresh == 0) return 0;
        long minutes = 0;
        while (head < tail) {
            int cur = queue[head++];
            int x = cur / M;
            int y = cur - x * M;
            int nd = dist[cur] + 1;
            if (x > 0 && dist[cur - M] == -1 && grid[x - 1][y] == 1) {
                dist[cur - M] = nd;
                queue[tail++] = cur - M;
                --fresh;
                if (nd > minutes) minutes = nd;
            }
            if (x + 1 < N && dist[cur + M] == -1 && grid[x + 1][y] == 1) {
                dist[cur + M] = nd;
                queue[tail++] = cur + M;
                --fresh;
                if (nd > minutes) minutes = nd;
            }
            if (y > 0 && dist[cur - 1] == -1 && grid[x][y - 1] == 1) {
                dist[cur - 1] = nd;
                queue[tail++] = cur - 1;
                --fresh;
                if (nd > minutes) minutes = nd;
            }
            if (y + 1 < M && dist[cur + 1] == -1 && grid[x][y + 1] == 1) {
                dist[cur + 1] = nd;
                queue[tail++] = cur + 1;
                --fresh;
                if (nd > minutes) minutes = nd;
            }
        }
        return fresh > 0 ? -1 : minutes;
    }
