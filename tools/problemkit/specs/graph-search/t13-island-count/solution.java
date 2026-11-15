    static long solve(long n, long m, long[][] grid) {
        int N = (int) n;
        int M = (int) m;
        int total = N * M;
        boolean[] seen = new boolean[total];
        int[] stack = new int[total];
        long count = 0;
        for (int s = 0; s < total; ++s) {
            if (seen[s]) continue;
            int sx = s / M;
            int sy = s - sx * M;
            if (grid[sx][sy] != 1) continue;
            ++count;
            int top = 0;
            stack[top++] = s;
            seen[s] = true;
            while (top > 0) {
                int cur = stack[--top];
                int x = cur / M;
                int y = cur - x * M;
                int nxt = cur - M;
                if (x > 0 && !seen[nxt] && grid[x - 1][y] == 1) {
                    seen[nxt] = true;
                    stack[top++] = nxt;
                }
                nxt = cur + M;
                if (x + 1 < N && !seen[nxt] && grid[x + 1][y] == 1) {
                    seen[nxt] = true;
                    stack[top++] = nxt;
                }
                nxt = cur - 1;
                if (y > 0 && !seen[nxt] && grid[x][y - 1] == 1) {
                    seen[nxt] = true;
                    stack[top++] = nxt;
                }
                nxt = cur + 1;
                if (y + 1 < M && !seen[nxt] && grid[x][y + 1] == 1) {
                    seen[nxt] = true;
                    stack[top++] = nxt;
                }
            }
        }
        return count;
    }
