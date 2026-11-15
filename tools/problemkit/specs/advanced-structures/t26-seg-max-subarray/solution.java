    static long[] solve(long n, long[] a, long q, long[][] ops) {
        final long NEG = -(1L << 61);
        int size = 1;
        while (size < n) size <<= 1;
        long[] sum = new long[size << 1];
        long[] pre = new long[size << 1];
        long[] suf = new long[size << 1];
        long[] bst = new long[size << 1];
        Arrays.fill(pre, NEG);
        Arrays.fill(suf, NEG);
        Arrays.fill(bst, NEG);
        for (int i = 0; i < (int) n; ++i) {
            int k = size + i;
            long v = a[i];
            sum[k] = v;
            pre[k] = v;
            suf[k] = v;
            bst[k] = v;
        }
        for (int k = size - 1; k >= 1; --k) {
            int lc = k << 1, rc = lc | 1;
            sum[k] = sum[lc] + sum[rc];
            pre[k] = Math.max(pre[lc], sum[lc] + pre[rc]);
            suf[k] = Math.max(suf[rc], sum[rc] + suf[lc]);
            bst[k] = Math.max(Math.max(bst[lc], bst[rc]), suf[lc] + pre[rc]);
        }

        long[] answer = new long[(int) q];
        for (int j = 0; j < (int) q; ++j) {
            int l = size + (int) ops[j][0] - 1;
            int r = size + (int) ops[j][1];
            long ls = 0, lp = NEG, lsf = NEG, lb = NEG;
            long rs = 0, rp = NEG, rsf = NEG, rb = NEG;
            while (l < r) {
                if ((l & 1) == 1) {
                    long ns = ls + sum[l];
                    long np = Math.max(lp, ls + pre[l]);
                    long nsf = Math.max(suf[l], sum[l] + lsf);
                    long nb = Math.max(Math.max(lb, bst[l]), lsf + pre[l]);
                    ls = ns; lp = np; lsf = nsf; lb = nb;
                    ++l;
                }
                if ((r & 1) == 1) {
                    --r;
                    long ns = sum[r] + rs;
                    long np = Math.max(pre[r], sum[r] + rp);
                    long nsf = Math.max(rs + suf[r], rsf);
                    long nb = Math.max(Math.max(bst[r], rb), suf[r] + rp);
                    rs = ns; rp = np; rsf = nsf; rb = nb;
                }
                l >>= 1;
                r >>= 1;
            }
            long best = Math.max(lb, rb);
            best = Math.max(best, lsf + rp);
            answer[j] = best;
        }
        return answer;
    }
