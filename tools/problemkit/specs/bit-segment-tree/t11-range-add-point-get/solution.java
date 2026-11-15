    static long[] solve(long n, long[] a, long q, long[][] ops) {
        int size = (int) n;
        long[] tree = new long[size + 2];
        long[] buffer = new long[(int) q];
        int count = 0;
        for (int j = 0; j < (int) q; ++j) {
            long t = ops[j][0];
            int l = (int) ops[j][1];
            int r = (int) ops[j][2];
            long v = ops[j][3];
            if (t == 1) {
                for (int i = l; i <= size; i += i & -i) tree[i] += v;
                for (int i = r + 1; i <= size; i += i & -i) tree[i] -= v;
            } else {
                long sum = 0;
                for (int i = l; i > 0; i -= i & -i) sum += tree[i];
                buffer[count++] = a[l - 1] + sum;
            }
        }
        long[] answer = new long[count];
        for (int i = 0; i < count; ++i) answer[i] = buffer[i];
        return answer;
    }
