    static long solve(long m, long[] nums, String[] ops) {
        final long NEG = -4000000000000000000L;
        final long POS = 4000000000000000000L;
        int mm = (int) m;
        long[][] mx = new long[mm][mm];
        long[][] mn = new long[mm][mm];
        for (int i = 0; i < mm; ++i) {
            for (int j = 0; j < mm; ++j) {
                mx[i][j] = NEG;
                mn[i][j] = POS;
            }
            mx[i][i] = nums[i];
            mn[i][i] = nums[i];
        }
        for (int len = 2; len <= mm; ++len) {
            for (int i = 0; i + len - 1 < mm; ++i) {
                int j = i + len - 1;
                for (int k = i; k < j; ++k) {
                    long a1 = mx[i][k], a2 = mn[i][k];
                    long b1 = mx[k + 1][j], b2 = mn[k + 1][j];
                    long[] cand = new long[4];
                    int cnt = 0;
                    if (ops[k].equals("+")) {
                        cand[cnt++] = a1 + b1;
                        cand[cnt++] = a2 + b2;
                    } else if (ops[k].equals("-")) {
                        cand[cnt++] = a1 - b2;
                        cand[cnt++] = a2 - b1;
                    } else {
                        cand[cnt++] = a1 * b1;
                        cand[cnt++] = a1 * b2;
                        cand[cnt++] = a2 * b1;
                        cand[cnt++] = a2 * b2;
                    }
                    for (int t = 0; t < cnt; ++t) {
                        if (cand[t] > mx[i][j]) mx[i][j] = cand[t];
                        if (cand[t] < mn[i][j]) mn[i][j] = cand[t];
                    }
                }
            }
        }
        return mx[0][mm - 1];
    }
