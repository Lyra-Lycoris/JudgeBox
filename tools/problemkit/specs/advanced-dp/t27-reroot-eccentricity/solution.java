    static long[] solve(long n, long[] p) {
        int N = (int) n;
        long[] down = new long[N + 1];
        long[] up = new long[N + 1];
        long[] best1 = new long[N + 1];
        long[] best2 = new long[N + 1];
        int[] who = new int[N + 1];
        for (int i = N; i >= 2; --i) {
            int par = (int) p[i - 2];
            long val = down[i] + 1;
            if (val > best1[par]) {
                best2[par] = best1[par];
                best1[par] = val;
                who[par] = i;
            } else if (val > best2[par]) {
                best2[par] = val;
            }
            if (val > down[par]) down[par] = val;
        }
        for (int i = 2; i <= N; ++i) {
            int par = (int) p[i - 2];
            long sib = (who[par] == i) ? best2[par] : best1[par];
            long base = Math.max(up[par], sib);
            up[i] = base + 1;
        }
        long[] ans = new long[N];
        for (int i = 1; i <= N; ++i) ans[i - 1] = Math.max(down[i], up[i]);
        return ans;
    }
