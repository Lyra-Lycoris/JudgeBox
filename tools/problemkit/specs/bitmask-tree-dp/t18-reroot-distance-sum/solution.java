    static long[] solve(long n, long[] p) {
        int N = (int) n;
        long[] sz = new long[N + 1];
        long[] depth = new long[N + 1];
        long[] f = new long[N + 1];
        for (int i = 1; i <= N; ++i) sz[i] = 1;
        for (int i = N; i >= 2; --i) sz[(int) p[i - 2]] += sz[i];
        for (int i = 2; i <= N; ++i) {
            depth[i] = depth[(int) p[i - 2]] + 1;
            f[1] += depth[i];
        }
        for (int i = 2; i <= N; ++i) {
            int par = (int) p[i - 2];
            f[i] = f[par] + n - 2 * sz[i];
        }
        long[] answer = new long[N];
        for (int i = 1; i <= N; ++i) answer[i - 1] = f[i];
        return answer;
    }
