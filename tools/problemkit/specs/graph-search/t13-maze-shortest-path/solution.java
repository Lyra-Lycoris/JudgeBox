    static long solve(long n, long m, long[][] grid) {
        int N = (int) n;
        int M = (int) m;
        if (N <= 0 || M <= 0) return -1;
        if (grid[0][0] != 0 || grid[N - 1][M - 1] != 0) return -1;
        int total = N * M;
        int[] dist = new int[total];
        Arrays.fill(dist, -1);
        int[] queue = new int[total];
        int head = 0, tail = 0;
        dist[0] = 0;
        queue[tail++] = 0;
        while (head < tail) {
            int cur = queue[head++];
            int x = cur / M;
            int y = cur - x * M;
            int d = dist[cur] + 1;
            if (x > 0 && grid[x - 1][y] == 0 && dist[cur - M] == -1) {
                dist[cur - M] = d;
                queue[tail++] = cur - M;
            }
            if (x + 1 < N && grid[x + 1][y] == 0 && dist[cur + M] == -1) {
                dist[cur + M] = d;
                queue[tail++] = cur + M;
            }
            if (y > 0 && grid[x][y - 1] == 0 && dist[cur - 1] == -1) {
                dist[cur - 1] = d;
                queue[tail++] = cur - 1;
            }
            if (y + 1 < M && grid[x][y + 1] == 0 && dist[cur + 1] == -1) {
                dist[cur + 1] = d;
                queue[tail++] = cur + 1;
            }
        }
        return dist[total - 1];
    }
