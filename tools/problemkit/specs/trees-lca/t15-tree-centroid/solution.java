    static long solve(long n, long[] e) {
        if (n == 1) return 1;
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
        int[] order = new int[N];
        boolean[] visited = new boolean[N + 1];
        for (int v = 1; v <= N; ++v) parent[v] = 1;
        int cnt = 0;
        order[cnt++] = 1;
        visited[1] = true;
        for (int i = 0; i < cnt; ++i) {
            int u = order[i];
            for (int j = head[u]; j < head[u + 1]; ++j) {
                int v = adj[j];
                if (!visited[v]) {
                    visited[v] = true;
                    parent[v] = u;
                    order[cnt++] = v;
                }
            }
        }

        long[] size = new long[N + 1];
        for (int v = 1; v <= N; ++v) size[v] = 1;
        for (int i = N - 1; i > 0; --i) {
            int v = order[i];
            size[parent[v]] += size[v];
        }
        long[] maxPart = new long[N + 1];
        for (int v = 1; v <= N; ++v) maxPart[v] = n - size[v];
        for (int i = 1; i < N; ++i) {
            int v = order[i], p = parent[v];
            if (size[v] > maxPart[p]) maxPart[p] = size[v];
        }
        for (int v = 1; v <= N; ++v) {
            if (maxPart[v] * 2 <= n) return v;
        }
        return 1;
    }
