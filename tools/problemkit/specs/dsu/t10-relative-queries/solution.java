    static int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    static void unite(int[] parent, int[] size, int a, int b) {
        a = find(parent, a);
        b = find(parent, b);
        if (a == b) return;
        if (size[a] < size[b]) {
            int t = a;
            a = b;
            b = t;
        }
        parent[b] = a;
        size[a] += size[b];
    }

    static long solve(long n, long k, long[][] rel, long q, long[][] qs) {
        int nn = (int) n;
        int[] parent = new int[nn + 1];
        int[] size = new int[nn + 1];
        for (int i = 0; i <= nn; ++i) {
            parent[i] = i;
            size[i] = 1;
        }
        int kk = (int) k;
        for (int i = 0; i < kk; ++i) {
            unite(parent, size, (int) rel[i][0], (int) rel[i][1]);
        }
        long answer = 0;
        int qq = (int) q;
        for (int i = 0; i < qq; ++i) {
            if (find(parent, (int) qs[i][0]) == find(parent, (int) qs[i][1])) ++answer;
        }
        return answer;
    }
