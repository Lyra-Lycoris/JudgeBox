    static long solve(long n, long m, long[][] g) {
        int rows = (int) n, cols = (int) m;
        int total = rows * cols;
        int[] cell = new int[total];
        for (int i = 0; i < rows; ++i)
            for (int j = 0; j < cols; ++j) cell[i * cols + j] = (int) g[i][j];
        final int INF = 1 << 30;
        int[] dist = new int[total];
        Arrays.fill(dist, INF);
        ArrayDeque<Integer> dq = new ArrayDeque<>();
        dist[0] = 0;
        dq.addLast(0);
        while (!dq.isEmpty()) {
            int u = dq.pollFirst();
            int du = dist[u];
            int r = u / cols, c = u % cols;
            int[] nb = new int[4];
            int count = 0;
            if (r > 0) nb[count++] = u - cols;
            if (r + 1 < rows) nb[count++] = u + cols;
            if (c > 0) nb[count++] = u - 1;
            if (c + 1 < cols) nb[count++] = u + 1;
            for (int k = 0; k < count; ++k) {
                int v = nb[k];
                int nd = du + cell[v];
                if (nd < dist[v]) {
                    dist[v] = nd;
                    if (cell[v] == 0) dq.addFirst(v);
                    else dq.addLast(v);
                }
            }
        }
        return dist[total - 1];
    }
