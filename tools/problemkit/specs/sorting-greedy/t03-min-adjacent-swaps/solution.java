    static long solve(long n, long[] a) {
        final long SHIFT = 1000000000L;
        final long BASE = 1048576L;
        long[] keys = new long[(int) n];
        for (int i = 0; i < n; ++i) keys[i] = (a[i] + SHIFT) * BASE + i;
        Arrays.sort(keys);
        int[] perm = new int[(int) n];
        for (int p = 0; p < n; ++p) perm[(int) (keys[p] % BASE)] = p + 1;
        int[] tree = new int[(int) n + 1];
        long total = 0;
        for (int i = 0; i < n; ++i) {
            int v = perm[i];
            int sum = 0;
            for (int x = v; x > 0; x -= x & (-x)) sum += tree[x];
            total += i - sum;
            for (int x = v; x <= n; x += x & (-x)) tree[x] += 1;
        }
        return total;
    }
