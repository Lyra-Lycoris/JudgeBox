    static long solve(long n, long m, long[][] e) {
        int N = (int) n;
        int M = (int) m;
        int[] deg = new int[N + 1];
        int[] indeg = new int[N + 1];
        int[] start = new int[N + 2];
        int[] rstart = new int[N + 2];
        boolean[] hasSelf = new boolean[N + 1];
        for (int i = 0; i < M; ++i) {
            int a = (int) e[i][0];
            int b = (int) e[i][1];
            ++deg[a];
            ++indeg[b];
            if (a == b) hasSelf[a] = true;
        }
        for (int v = 1; v <= N; ++v) {
            start[v + 1] = start[v] + deg[v];
            rstart[v + 1] = rstart[v] + indeg[v];
        }
        int[] cursor = start.clone();
        int[] rcursor = rstart.clone();
        int[] adj = new int[Math.max(M, 1)];
        int[] radj = new int[Math.max(M, 1)];
        for (int i = 0; i < M; ++i) {
            int a = (int) e[i][0];
            int b = (int) e[i][1];
            adj[cursor[a]++] = b;
            radj[rcursor[b]++] = a;
        }
        boolean[] visited = new boolean[N + 1];
        int[] order = new int[N];
        int[] stackArr = new int[N];
        int[] it = start.clone();
        int on = 0;
        for (int s = 1; s <= N; ++s) {
            if (visited[s]) continue;
            visited[s] = true;
            int sp = 1;
            stackArr[0] = s;
            while (sp > 0) {
                int u = stackArr[sp - 1];
                if (it[u] < start[u + 1]) {
                    int v = adj[it[u]++];
                    if (!visited[v]) {
                        visited[v] = true;
                        stackArr[sp++] = v;
                    }
                } else {
                    order[on++] = u;
                    --sp;
                }
            }
        }
        int[] comp = new int[N + 1];
        Arrays.fill(comp, -1);
        int[] sizes = new int[N];
        int compCount = 0;
        for (int idx = N - 1; idx >= 0; --idx) {
            int s = order[idx];
            if (comp[s] != -1) continue;
            int cid = compCount++;
            comp[s] = cid;
            int size = 0;
            int sp = 1;
            stackArr[0] = s;
            while (sp > 0) {
                int u = stackArr[--sp];
                ++size;
                for (int k = rstart[u]; k < rstart[u + 1]; ++k) {
                    int v = radj[k];
                    if (comp[v] == -1) {
                        comp[v] = cid;
                        stackArr[sp++] = v;
                    }
                }
            }
            sizes[cid] = size;
        }
        long answer = 0;
        for (int cid = 0; cid < compCount; ++cid) {
            if (sizes[cid] > 1) answer += sizes[cid];
        }
        for (int v = 1; v <= N; ++v) {
            if (hasSelf[v] && sizes[comp[v]] == 1) ++answer;
        }
        return answer;
    }
