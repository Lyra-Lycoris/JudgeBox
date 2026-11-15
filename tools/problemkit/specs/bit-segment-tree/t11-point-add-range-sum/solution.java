    static long[] solve(long n, long[] a, long q, long[][] ops) {
        int size = (int) n;
        long[] tree = new long[size + 1];
        for (int i = 1; i <= size; ++i) {
            tree[i] += a[i - 1];
            int up = i + (i & -i);
            if (up <= size) tree[up] += tree[i];
        }
        long[] buffer = new long[(int) q];
        int count = 0;
        for (int j = 0; j < (int) q; ++j) {
            if (ops[j][0] == 1) {
                int i = (int) ops[j][1];
                long v = ops[j][2];
                while (i <= size) {
                    tree[i] += v;
                    i += i & -i;
                }
            } else {
                long sum = 0;
                for (int i = (int) ops[j][2]; i > 0; i -= i & -i) sum += tree[i];
                for (int i = (int) ops[j][1] - 1; i > 0; i -= i & -i) sum -= tree[i];
                buffer[count++] = sum;
            }
        }
        long[] answer = new long[count];
        for (int i = 0; i < count; ++i) answer[i] = buffer[i];
        return answer;
    }
