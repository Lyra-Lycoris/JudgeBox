    static boolean solve(long n, long m, long[][] e) {
        int N = (int) n;
        int M = (int) m;
        int[] deg = new int[N + 1];
        int[] indeg = new int[N + 1];
        int[] start = new int[N + 2];
        for (int i = 0; i < M; ++i) {
            int a = (int) e[i][0];
            int b = (int) e[i][1];
            ++deg[a];
            ++indeg[b];
        }
        for (int v = 1; v <= N; ++v) start[v + 1] = start[v] + deg[v];
        int[] cursor = start.clone();
        int[] adj = new int[Math.max(M, 1)];
        for (int i = 0; i < M; ++i) {
            int a = (int) e[i][0];
            int b = (int) e[i][1];
            adj[cursor[a]++] = b;
        }
        int[] queue = new int[N];
        int head = 0, tail = 0;
        for (int v = 1; v <= N; ++v) {
            if (indeg[v] == 0) queue[tail++] = v;
        }
        long seen = 0;
        while (head < tail) {
            int u = queue[head++];
            ++seen;
            for (int k = start[u]; k < start[u + 1]; ++k) {
                int b = adj[k];
                if (--indeg[b] == 0) queue[tail++] = b;
            }
        }
        return seen == n;
    }
