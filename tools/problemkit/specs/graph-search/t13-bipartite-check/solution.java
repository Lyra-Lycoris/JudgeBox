    static boolean solve(long n, long m, long[][] e) {
        int N = (int) n;
        int M = (int) m;
        int[] deg = new int[N + 1];
        int[] start = new int[N + 2];
        for (int i = 0; i < M; ++i) {
            int a = (int) e[i][0];
            int b = (int) e[i][1];
            ++deg[a];
            ++deg[b];
        }
        for (int v = 1; v <= N; ++v) start[v + 1] = start[v] + deg[v];
        int[] cursor = start.clone();
        int[] adj = new int[Math.max(2 * M, 1)];
        for (int i = 0; i < M; ++i) {
            int a = (int) e[i][0];
            int b = (int) e[i][1];
            adj[cursor[a]++] = b;
            adj[cursor[b]++] = a;
        }
        int[] color = new int[N + 1];
        Arrays.fill(color, -1);
        int[] queue = new int[N];
        for (int s = 1; s <= N; ++s) {
            if (color[s] != -1) continue;
            color[s] = 0;
            int head = 0, tail = 0;
            queue[tail++] = s;
            while (head < tail) {
                int u = queue[head++];
                for (int k = start[u]; k < start[u + 1]; ++k) {
                    int v = adj[k];
                    if (color[v] == -1) {
                        color[v] = color[u] ^ 1;
                        queue[tail++] = v;
                    } else if (color[v] == color[u]) {
                        return false;
                    }
                }
            }
        }
        return true;
    }
