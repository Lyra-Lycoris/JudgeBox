    static long[] solve(long n, long[] a, long q, long[][] ops) {
        final long NEG = -(1L << 61);
        int size = 1;
        while (size < (int) n) size <<= 1;

        long[] total = new long[size << 1];
        long[] pref = new long[size << 1];
        long[] suff = new long[size << 1];
        long[] best = new long[size << 1];
        Arrays.fill(pref, NEG);
        Arrays.fill(suff, NEG);
        Arrays.fill(best, NEG);
        for (int i = 0; i < (int) n; ++i) {
            int k = size + i;
            long v = a[i];
            total[k] = v;
            pref[k] = v;
            suff[k] = v;
            best[k] = v;
        }
        for (int k = size - 1; k > 0; --k) {
            int lc = k << 1, rc = lc | 1;
            total[k] = total[lc] + total[rc];
            pref[k] = Math.max(pref[lc], total[lc] + pref[rc]);
            suff[k] = Math.max(suff[rc], total[rc] + suff[lc]);
            best[k] = Math.max(Math.max(best[lc], best[rc]), suff[lc] + pref[rc]);
        }

        long[] answer = new long[(int) q];
        int count = 0;
        for (int j = 0; j < (int) q; ++j) {
            long t = ops[j][0];
            int x = (int) ops[j][1];
            long y = ops[j][2];
            if (t == 1) {
                int k = size + x - 1;
                total[k] = y;
                pref[k] = y;
                suff[k] = y;
                best[k] = y;
                for (k >>= 1; k > 0; k >>= 1) {
                    int lc = k << 1, rc = lc | 1;
                    total[k] = total[lc] + total[rc];
                    pref[k] = Math.max(pref[lc], total[lc] + pref[rc]);
                    suff[k] = Math.max(suff[rc], total[rc] + suff[lc]);
                    best[k] = Math.max(Math.max(best[lc], best[rc]), suff[lc] + pref[rc]);
                }
            } else {
                int l = size + x - 1;
                int r = size + (int) y;
                long ls = 0, lp = NEG, lsf = NEG, lb = NEG;
                long rs = 0, rp = NEG, rsf = NEG, rb = NEG;
                while (l < r) {
                    if ((l & 1) != 0) {
                        long ns = ls + total[l];
                        long np = Math.max(lp, ls + pref[l]);
                        long nsf = Math.max(suff[l], total[l] + lsf);
                        long nb = Math.max(Math.max(lb, best[l]), lsf + pref[l]);
                        ls = ns;
                        lp = np;
                        lsf = nsf;
                        lb = nb;
                        ++l;
                    }
                    if ((r & 1) != 0) {
                        --r;
                        long ns = total[r] + rs;
                        long np = Math.max(pref[r], total[r] + rp);
                        long nsf = Math.max(rsf, rs + suff[r]);
                        long nb = Math.max(Math.max(best[r], rb), suff[r] + rp);
                        rs = ns;
                        rp = np;
                        rsf = nsf;
                        rb = nb;
                    }
                    l >>= 1;
                    r >>= 1;
                }
                answer[count++] = Math.max(Math.max(lb, rb), lsf + rp);
            }
        }
        long[] result = new long[count];
        for (int i = 0; i < count; ++i) result[i] = answer[i];
        return result;
    }
