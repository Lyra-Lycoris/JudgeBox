    static long[] solve(long n, long[] a, long q, long[][] ops) {
        int sz = (int) n;
        long[] cur = Arrays.copyOf(a, sz);
        long[] bit = new long[sz + 1];
        for (int i = 1; i <= sz; ++i) {
            bit[i] += cur[i - 1];
            int j = i + (i & -i);
            if (j <= sz) bit[j] += bit[i];
        }

        int step0 = 1;
        while (((long) step0 << 1) <= n) step0 <<= 1;

        long[] answer = new long[(int) q];
        int count = 0;
        for (int k = 0; k < (int) q; ++k) {
            long t = ops[k][0], x = ops[k][1], v = ops[k][2];
            if (t == 1) {
                long delta = v - cur[(int) x - 1];
                cur[(int) x - 1] = v;
                for (int i = (int) x; i <= sz; i += i & -i) bit[i] += delta;
            } else {
                long need = x;
                int pos = 0;
                int step = step0;
                while (step > 0) {
                    int nxt = pos + step;
                    if (nxt <= sz && bit[nxt] < need) {
                        pos = nxt;
                        need -= bit[nxt];
                    }
                    step >>= 1;
                }
                answer[count++] = pos + 1;
            }
        }
        return Arrays.copyOf(answer, count);
    }
