    static long[] solve(long n, long[] a, long q, long[][] ops) {
        int sz = (int) n;
        int blockSize = (int) Math.sqrt((double) sz) + 1;
        int blocks = (sz + blockSize - 1) / blockSize;
        final long NEG = -(1L << 62);
        long[] val = Arrays.copyOf(a, sz);
        long[] lazy = new long[blocks];
        long[] best = new long[blocks];
        Arrays.fill(best, NEG);
        for (int i = 0; i < sz; ++i) {
            int b = i / blockSize;
            if (val[i] > best[b]) best[b] = val[i];
        }

        long[] answer = new long[(int) q];
        int count = 0;
        for (int k = 0; k < (int) q; ++k) {
            long t = ops[k][0];
            int l = (int) ops[k][1] - 1;
            int r = (int) ops[k][2] - 1;
            long x = ops[k][3];
            int bl = l / blockSize, br = r / blockSize;
            if (t == 1) {
                if (bl == br) {
                    for (int i = l; i <= r; ++i) val[i] += x;
                    best[bl] = NEG;
                    int hi = Math.min(sz, (bl + 1) * blockSize);
                    for (int i = bl * blockSize; i < hi; ++i) if (val[i] > best[bl]) best[bl] = val[i];
                } else {
                    for (int i = l; i < (bl + 1) * blockSize; ++i) val[i] += x;
                    best[bl] = NEG;
                    for (int i = bl * blockSize; i < (bl + 1) * blockSize; ++i) if (val[i] > best[bl]) best[bl] = val[i];
                    for (int i = br * blockSize; i <= r; ++i) val[i] += x;
                    best[br] = NEG;
                    int hi = Math.min(sz, (br + 1) * blockSize);
                    for (int i = br * blockSize; i < hi; ++i) if (val[i] > best[br]) best[br] = val[i];
                    for (int b = bl + 1; b < br; ++b) lazy[b] += x;
                }
            } else {
                long m = NEG;
                if (bl == br) {
                    for (int i = l; i <= r; ++i) {
                        long v = val[i] + lazy[bl];
                        if (v > m) m = v;
                    }
                } else {
                    for (int i = l; i < (bl + 1) * blockSize; ++i) {
                        long v = val[i] + lazy[bl];
                        if (v > m) m = v;
                    }
                    for (int i = br * blockSize; i <= r; ++i) {
                        long v = val[i] + lazy[br];
                        if (v > m) m = v;
                    }
                    for (int b = bl + 1; b < br; ++b) {
                        long v = best[b] + lazy[b];
                        if (v > m) m = v;
                    }
                }
                answer[count++] = m;
            }
        }
        return Arrays.copyOf(answer, count);
    }
