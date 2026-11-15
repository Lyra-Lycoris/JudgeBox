    static long solve(long n, long k, long[] a) {
        int N = (int) n;
        long[] dp = new long[N];
        int[] q = new int[N + 1];
        dp[0] = a[0];
        int head = 0, tail = 1;
        for (int i = 1; i < N; ++i) {
            long left = (long) i - k;
            while (head < tail && q[head] < left) ++head;
            dp[i] = a[i] + dp[q[head]];
            while (head < tail && dp[q[tail - 1]] >= dp[i]) --tail;
            q[tail++] = i;
        }
        return dp[N - 1];
    }
