    static ArrayList<ArrayList<Integer>> children;
    static long[] profits;
    static int limit;

    static long[] dfs(int u) {
        long[] f = new long[]{0L, u == 0 ? 0L : profits[u - 1]};
        int size = 1;
        for (int ch : children.get(u)) {
            long[] fc = dfs(ch);
            int sc = fc.length - 1;
            int newcap = Math.min(size + sc, limit);
            long[] g = new long[newcap + 1];
            Arrays.fill(g, Long.MIN_VALUE / 4);
            g[0] = 0;
            for (int j = 1; j <= size; ++j) {
                for (int t = 0; t <= sc && j + t <= newcap; ++t) {
                    long val = f[j] + fc[t];
                    if (val > g[j + t]) g[j + t] = val;
                }
            }
            f = g;
            size = newcap;
        }
        return f;
    }

    static long solve(long n, long k, long[] parent, long[] profit) {
        children = new ArrayList<ArrayList<Integer>>();
        for (int i = 0; i <= n; ++i) children.add(new ArrayList<Integer>());
        for (int i = 1; i <= n; ++i) children.get((int) parent[i - 1]).add(i);
        profits = profit;
        limit = (int) k + 1;
        return dfs(0)[limit];
    }
