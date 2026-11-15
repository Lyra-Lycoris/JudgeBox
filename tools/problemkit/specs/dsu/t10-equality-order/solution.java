    static int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    static boolean solve(long n, long k, long[][] cons) {
        int nn = (int) n;
        int kk = (int) k;
        int[] parent = new int[nn + 1];
        int[] size = new int[nn + 1];
        for (int i = 0; i <= nn; ++i) {
            parent[i] = i;
            size[i] = 1;
        }
        for (int i = 0; i < kk; ++i) {
            if (cons[i][0] != 0) continue;
            int a = find(parent, (int) cons[i][1]);
            int b = find(parent, (int) cons[i][2]);
            if (a == b) continue;
            if (size[a] < size[b]) {
                int t = a;
                a = b;
                b = t;
            }
            parent[b] = a;
            size[a] += size[b];
        }

        int[] id = new int[nn + 1];
        Arrays.fill(id, -1);
        int cnt = 0;
        for (int v = 1; v <= nn; ++v) {
            int r = find(parent, v);
            if (id[r] < 0) id[r] = cnt++;
        }

        int[] outdeg = new int[cnt];
        for (int i = 0; i < kk; ++i) {
            if (cons[i][0] != 1) continue;
            int u = id[find(parent, (int) cons[i][1])];
            int v = id[find(parent, (int) cons[i][2])];
            if (u == v) return false;
            ++outdeg[u];
        }

        int[] start = new int[cnt + 1];
        for (int i = 0; i < cnt; ++i) start[i + 1] = start[i] + outdeg[i];
        int[] to = new int[start[cnt]];
        int[] fill = new int[cnt];
        int[] indeg = new int[cnt];
        for (int i = 0; i < kk; ++i) {
            if (cons[i][0] != 1) continue;
            int u = id[find(parent, (int) cons[i][1])];
            int v = id[find(parent, (int) cons[i][2])];
            to[start[u] + fill[u]++] = v;
            ++indeg[v];
        }

        int[] order = new int[cnt];
        int head = 0, tail = 0;
        for (int i = 0; i < cnt; ++i) {
            if (indeg[i] == 0) order[tail++] = i;
        }
        int seen = 0;
        while (head < tail) {
            int u = order[head++];
            ++seen;
            for (int j = start[u]; j < start[u + 1]; ++j) {
                int v = to[j];
                if (--indeg[v] == 0) order[tail++] = v;
            }
        }
        return seen == cnt;
    }
