    static int bfsFarthest(int[] head, int[] adj, int n, int src, int[] dist) {
        for (int i = 0; i <= n; ++i) dist[i] = -1;
        int[] queue = new int[n + 1];
        int qh = 0, qt = 0;
        queue[qt++] = src;
        dist[src] = 0;
        while (qh < qt) {
            int u = queue[qh++];
            for (int i = head[u]; i < head[u + 1]; ++i) {
                int v = adj[i];
                if (dist[v] < 0) {
                    dist[v] = dist[u] + 1;
                    queue[qt++] = v;
                }
            }
        }
        int far = src;
        for (int i = 1; i <= n; ++i) {
            if (dist[i] > dist[far]) far = i;
        }
        return far;
    }

    static long solve(long n, long[] e) {
        if (n <= 1) return 0;
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
        int[] dist = new int[N + 1];
        int a = bfsFarthest(head, adj, N, 1, dist);
        int b = bfsFarthest(head, adj, N, a, dist);
        return dist[b];
    }
