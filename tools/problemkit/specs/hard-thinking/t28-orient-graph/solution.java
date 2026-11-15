    static int orientFind(int[] dsu, int x) {
        while (dsu[x] != x) {
            dsu[x] = dsu[dsu[x]];
            x = dsu[x];
        }
        return x;
    }

    static long[] solve(long n, long m, long[][] e) {
        int nn = (int) n;
        int mm = (int) m;
        int[] dsu = new int[nn + 1];
        int[] dsuSize = new int[nn + 1];
        for (int i = 0; i <= nn; ++i) {
            dsu[i] = i;
            dsuSize[i] = 1;
        }
        for (int i = 0; i < mm; ++i) {
            int a = orientFind(dsu, (int) e[i][0]);
            int b = orientFind(dsu, (int) e[i][1]);
            if (a == b) continue;
            if (dsuSize[a] < dsuSize[b]) {
                int t = a;
                a = b;
                b = t;
            }
            dsu[b] = a;
            dsuSize[a] += dsuSize[b];
        }

        int[] edgeCnt = new int[nn + 1];
        for (int i = 0; i < mm; ++i) edgeCnt[orientFind(dsu, (int) e[i][0])]++;
        for (int v = 1; v <= nn; ++v) {
            if (dsu[v] == v && edgeCnt[v] > dsuSize[v]) return new long[] {-1};
        }

        int[] head = new int[nn + 1];
        Arrays.fill(head, -1);
        int[] to = new int[2 * mm];
        int[] nxt = new int[2 * mm];
        int[] eid = new int[2 * mm];
        int cnt = 0;
        for (int i = 0; i < mm; ++i) {
            int a = (int) e[i][0];
            int b = (int) e[i][1];
            to[cnt] = b;
            eid[cnt] = i;
            nxt[cnt] = head[a];
            head[a] = cnt++;
            to[cnt] = a;
            eid[cnt] = i;
            nxt[cnt] = head[b];
            head[b] = cnt++;
        }

        boolean[] visited = new boolean[nn + 1];
        int[] parent = new int[nn + 1];
        int[] depth = new int[nn + 1];
        int[] pedge = new int[nn + 1];
        Arrays.fill(pedge, -1);
        int[] cur = new int[nn + 1];
        System.arraycopy(head, 0, cur, 0, nn + 1);
        long[] answer = new long[2 * mm];
        int[] stack = new int[nn + 1];
        for (int s = 1; s <= nn; ++s) {
            if (visited[s]) continue;
            visited[s] = true;
            parent[s] = 0;
            depth[s] = 0;
            int top = 0;
            stack[top++] = s;
            while (top > 0) {
                int u = stack[top - 1];
                int j = cur[u];
                if (j == -1) {
                    --top;
                    continue;
                }
                cur[u] = nxt[j];
                int v = to[j];
                int k = eid[j];
                if (k == pedge[u]) continue;
                if (!visited[v]) {
                    visited[v] = true;
                    parent[v] = u;
                    pedge[v] = k;
                    depth[v] = depth[u] + 1;
                    answer[2 * k] = u;
                    answer[2 * k + 1] = v;
                    stack[top++] = v;
                } else if (depth[v] < depth[u]) {
                    answer[2 * k] = u;
                    answer[2 * k + 1] = v;
                    int c = v;
                    while (parent[c] != 0) {
                        int k2 = pedge[c];
                        answer[2 * k2] = c;
                        answer[2 * k2 + 1] = parent[c];
                        c = parent[c];
                    }
                }
            }
        }
        return answer;
    }
