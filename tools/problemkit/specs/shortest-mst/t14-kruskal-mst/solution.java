    static long solve(long n, long m, long[][] e) {
        int nn = (int) n, mm = (int) m;
        int[] parent = new int[nn + 1];
        for (int i = 0; i <= nn; ++i) parent[i] = i;
        long[][] edges = e.clone();
        Arrays.sort(edges, (a, b) -> Long.compare(a[2], b[2]));
        long total = 0;
        long used = 0;
        for (int k = 0; k < mm && used < n - 1; ++k) {
            int u = (int) edges[k][0];
            int v = (int) edges[k][1];
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
            if (ru != rv) {
                parent[ru] = rv;
                total += edges[k][2];
                ++used;
            }
        }
        return total;
    }
