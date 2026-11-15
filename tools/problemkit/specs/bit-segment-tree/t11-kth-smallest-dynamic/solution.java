    static long[] solve(long q, long[][] ops) {
        int total = (int) q;
        int insertCount = 0;
        for (int i = 0; i < total; ++i) if (ops[i][0] == 1) insertCount++;
        long[] values = new long[insertCount];
        int at = 0;
        for (int i = 0; i < total; ++i) if (ops[i][0] == 1) values[at++] = ops[i][1];
        Arrays.sort(values);
        int m = 0;
        for (int i = 0; i < insertCount; ++i) {
            if (i == 0 || values[i] != values[i - 1]) values[m++] = values[i];
        }
        long[] tree = new long[m + 1];
        int highest = 0;
        while ((1L << (highest + 1)) <= m) ++highest;
        int step0 = m > 0 ? (1 << highest) : 0;

        long[] answer = new long[total];
        int count = 0;
        for (int j = 0; j < total; ++j) {
            long t = ops[j][0];
            long x = ops[j][1];
            if (t == 1 || t == 2) {
                int i = (int) (Arrays.binarySearch(values, 0, m, x) + 1);
                long delta = t == 1 ? 1 : -1;
                for (; i <= m; i += i & -i) tree[i] += delta;
            } else {
                long k = x;
                int pos = 0;
                int step = step0;
                while (step > 0) {
                    int nxt = pos + step;
                    if (nxt <= m && tree[nxt] < k) {
                        pos = nxt;
                        k -= tree[nxt];
                    }
                    step >>= 1;
                }
                answer[count++] = values[pos];
            }
        }
        long[] result = new long[count];
        for (int i = 0; i < count; ++i) result[i] = answer[i];
        return result;
    }
