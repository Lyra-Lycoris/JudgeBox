    static long[] solve(long n, long[] a, long q, long[][] queries) {
        int size = (int) n;
        int[] lg = new int[size + 1];
        for (int i = 2; i <= size; ++i) lg[i] = lg[i / 2] + 1;
        int levels = 1;
        while ((1L << levels) <= size) ++levels;
        long[][] table = new long[levels][];
        table[0] = a;
        for (int j = 1; j < levels; ++j) {
            int len = size - (1 << j) + 1;
            int half = 1 << (j - 1);
            long[] row = new long[len];
            long[] prev = table[j - 1];
            for (int i = 0; i < len; ++i) row[i] = Math.max(prev[i], prev[i + half]);
            table[j] = row;
        }
        long[] answer = new long[(int) q];
        for (int k = 0; k < (int) q; ++k) {
            int l = (int) queries[k][0];
            int r = (int) queries[k][1];
            int level = lg[r - l + 1];
            answer[k] = Math.max(table[level][l - 1], table[level][r - (1 << level)]);
        }
        return answer;
    }
