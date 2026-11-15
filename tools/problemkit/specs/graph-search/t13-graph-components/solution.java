    static long solve(long n, long m, long[][] e) {
        int N = (int) n;
        int[] parent = new int[N + 1];
        int[] rank = new int[N + 1];
        for (int i = 0; i <= N; ++i) parent[i] = i;
        long count = n;
        for (int i = 0; i < (int) m; ++i) {
            int a = (int) e[i][0];
            int b = (int) e[i][1];
            while (parent[a] != a) {
                parent[a] = parent[parent[a]];
                a = parent[a];
            }
            while (parent[b] != b) {
                parent[b] = parent[parent[b]];
                b = parent[b];
            }
            if (a == b) continue;
            if (rank[a] < rank[b]) {
                int t = a;
                a = b;
                b = t;
            }
            parent[b] = a;
            if (rank[a] == rank[b]) ++rank[a];
            --count;
        }
        return count;
    }
