    static long[] solve(long n, long[] e, long q, long[] queries) {
        int N = (int) n;
        int m = e.length / 2;
        int[] deg = new int[N + 2];
        for (int i = 0; i < m; ++i) {
            deg[(int) e[2 * i]]++;
            deg[(int) e[2 * i + 1]]++;
        }
        int[] head = new int[N + 2];
        for (int i = 1; i <= N; ++i) head[i + 1] = head[i] + deg[i];
        int[] adj = new int[2 * m];
        int[] pos = head.clone();
        for (int i = 0; i < m; ++i) {
            int u = (int) e[2 * i], v = (int) e[2 * i + 1];
            adj[pos[u]++] = v;
            adj[pos[v]++] = u;
        }

        int[] parent = new int[N + 1];
        int[] depth = new int[N + 1];
        boolean[] visited = new boolean[N + 1];
        int[] queue = new int[N + 1];
        for (int v = 1; v <= N; ++v) parent[v] = 1;
        int qh = 0, qt = 0;
        queue[qt++] = 1;
        visited[1] = true;
        while (qh < qt) {
            int u = queue[qh++];
            for (int i = head[u]; i < head[u + 1]; ++i) {
                int v = adj[i];
                if (!visited[v]) {
                    visited[v] = true;
                    parent[v] = u;
                    depth[v] = depth[u] + 1;
                    queue[qt++] = v;
                }
            }
        }

        int LOG = 1;
        while ((1 << LOG) <= N) ++LOG;
        int[][] up = new int[LOG][N + 1];
        for (int v = 1; v <= N; ++v) up[0][v] = parent[v];
        for (int k = 1; k < LOG; ++k)
            for (int v = 1; v <= N; ++v) up[k][v] = up[k - 1][up[k - 1][v]];

        long[] answer = new long[(int) q];
        for (int t = 0; t < (int) q; ++t) {
            int u = (int) queries[2 * t], v = (int) queries[2 * t + 1];
            int du = depth[u], dv = depth[v];
            int a = u, b = v;
            if (depth[a] < depth[b]) { int tmp = a; a = b; b = tmp; }
            int diff = depth[a] - depth[b];
            for (int k = 0; k < LOG; ++k)
                if (((diff >> k) & 1) != 0) a = up[k][a];
            if (a != b) {
                for (int k = LOG - 1; k >= 0; --k) {
                    if (up[k][a] != up[k][b]) {
                        a = up[k][a];
                        b = up[k][b];
                    }
                }
                a = up[0][a];
            }
            answer[t] = (long) du + dv - 2L * depth[a];
        }
        return answer;
    }
