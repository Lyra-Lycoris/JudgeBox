    static long[] solve(long n, long m, long q, long[][] e, long[][] queries) {
        int nn = (int) n, mm = (int) m, qq = (int) q;
        int[] parent = new int[nn + 1];
        for (int i = 0; i <= nn; ++i) parent[i] = i;
        Integer[] order = new Integer[mm];
        for (int i = 0; i < mm; ++i) order[i] = i;
        Arrays.sort(order, (a, b) -> Long.compare(e[a][2], e[b][2]));
        int[] head = new int[nn + 1];
        Arrays.fill(head, -1);
        int[] to = new int[2 * (nn - 1)];
        int[] nxt = new int[2 * (nn - 1)];
        long[] wt = new long[2 * (nn - 1)];
        int cnt = 0;
        long used = 0;
        for (int k = 0; k < mm && used < n - 1; ++k) {
            int idx = order[k];
            int u = (int) e[idx][0], v = (int) e[idx][1];
            int ru = u;
            while (parent[ru] != ru) {
                parent[ru] = parent[parent[ru]];
                ru = parent[ru];
            }
            int rv = v;
            while (parent[rv] != rv) {
                parent[rv] = parent[parent[rv]];
                rv = parent[rv];
            }
            if (ru == rv) continue;
            parent[ru] = rv;
            to[cnt] = v; wt[cnt] = e[idx][2]; nxt[cnt] = head[u]; head[u] = cnt; ++cnt;
            to[cnt] = u; wt[cnt] = e[idx][2]; nxt[cnt] = head[v]; head[v] = cnt; ++cnt;
            ++used;
        }
        int LOG = 1;
        while ((1L << LOG) <= n) ++LOG;
        int[][] up = new int[LOG][nn + 1];
        long[][] mx = new long[LOG][nn + 1];
        int[] depth = new int[nn + 1];
        boolean[] seen = new boolean[nn + 1];
        int[] stack = new int[nn];
        int top = 0;
        seen[1] = true;
        stack[top++] = 1;
        while (top > 0) {
            int u = stack[--top];
            for (int i = head[u]; i != -1; i = nxt[i]) {
                int v = to[i];
                if (seen[v]) continue;
                seen[v] = true;
                depth[v] = depth[u] + 1;
                up[0][v] = u;
                mx[0][v] = wt[i];
                stack[top++] = v;
            }
        }
        for (int k = 1; k < LOG; ++k) {
            for (int v = 1; v <= nn; ++v) {
                int mid = up[k - 1][v];
                up[k][v] = up[k - 1][mid];
                mx[k][v] = Math.max(mx[k - 1][v], mx[k - 1][mid]);
            }
        }
        long[] answer = new long[qq];
        for (int t = 0; t < qq; ++t) {
            int u = (int) queries[t][0], v = (int) queries[t][1];
            long best = 0;
            if (depth[u] < depth[v]) { int tmp = u; u = v; v = tmp; }
            int diff = depth[u] - depth[v];
            for (int k = 0; diff != 0; ++k, diff >>= 1) {
                if ((diff & 1) != 0) {
                    best = Math.max(best, mx[k][u]);
                    u = up[k][u];
                }
            }
            if (u != v) {
                for (int k = LOG - 1; k >= 0; --k) {
                    if (up[k][u] != up[k][v]) {
                        best = Math.max(best, Math.max(mx[k][u], mx[k][v]));
                        u = up[k][u];
                        v = up[k][v];
                    }
                }
                best = Math.max(best, Math.max(mx[0][u], mx[0][v]));
            }
            answer[t] = best;
        }
        return answer;
    }
