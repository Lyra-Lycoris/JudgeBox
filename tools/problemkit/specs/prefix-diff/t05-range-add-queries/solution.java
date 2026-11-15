    static long[] solve(long n, long[] a, long q, long[][] ops) {
        int size = (int) n;
        long[] diff = new long[size + 1];
        for (int j = 0; j < (int) q; ++j) {
            int l = (int) ops[j][0];
            int r = (int) ops[j][1];
            long v = ops[j][2];
            diff[l - 1] += v;
            diff[r] -= v;
        }
        long[] answer = new long[size];
        long cur = 0;
        for (int i = 0; i < size; ++i) {
            cur += diff[i];
            answer[i] = a[i] + cur;
        }
        return answer;
    }
