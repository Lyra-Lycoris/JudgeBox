    static long[] solve(long n, long m, long[] r, long[] c) {
        final long SHIFT = 100000L;
        final long BIG = 99999L;
        int rows = (int) n;
        int cols = (int) m;
        long[] rem = new long[cols];
        System.arraycopy(c, 0, rem, 0, cols);
        long[] result = new long[rows * cols];
        long[] rowKeys = new long[rows];
        for (int i = 0; i < rows; ++i) rowKeys[i] = r[i] * SHIFT + (BIG - i);
        java.util.Arrays.sort(rowKeys);
        long[] colKeys = new long[cols];
        for (int t = rows - 1; t >= 0; --t) {
            long key = rowKeys[t];
            int i = (int) (BIG - key % SHIFT);
            int need = (int) (key / SHIFT);
            if (need == 0) continue;
            for (int j = 0; j < cols; ++j) colKeys[j] = rem[j] * SHIFT + (BIG - j);
            java.util.Arrays.sort(colKeys);
            int base = i * cols;
            for (int p = 0; p < need; ++p) {
                long ck = colKeys[cols - 1 - p];
                int j = (int) (BIG - ck % SHIFT);
                result[base + j] = 1;
                rem[j] -= 1;
            }
        }
        return result;
    }
