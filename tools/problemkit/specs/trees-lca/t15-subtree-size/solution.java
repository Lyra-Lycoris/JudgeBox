    static long[] solve(long n, long[] p) {
        int N = (int) n;
        long[] size = new long[N + 1];
        for (int v = 1; v <= N; ++v) size[v] = 1;
        for (int v = N; v >= 2; --v) {
            size[(int) p[v - 2]] += size[v];
        }
        long[] answer = new long[N];
        for (int i = 1; i <= N; ++i) answer[i - 1] = size[i];
        return answer;
    }
