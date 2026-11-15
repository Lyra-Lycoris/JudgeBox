    static long[] solve(long n, long m, long[][] a, long q, long[][] ops) {
        int r = (int) n, c = (int) m;
        long[][] pre = new long[r + 1][c + 1];
        for (int i = 1; i <= r; ++i) {
            long rowSum = 0;
            for (int j = 1; j <= c; ++j) {
                rowSum += a[i - 1][j - 1];
                pre[i][j] = pre[i - 1][j] + rowSum;
            }
        }

        long[][] bit = new long[r + 1][c + 1];
        for (int i = 1; i <= r; ++i) {
            int li = i - (i & -i);
            for (int j = 1; j <= c; ++j) {
                int lj = j - (j & -j);
                bit[i][j] = pre[i][j] - pre[li][j] - pre[i][lj] + pre[li][lj];
            }
        }

        long[] answer = new long[(int) q];
        int count = 0;
        for (int k = 0; k < (int) q; ++k) {
            long t = ops[k][0];
            int x = (int) ops[k][1], y = (int) ops[k][2];
            if (t == 1) {
                long v = ops[k][3];
                for (int i = x; i <= r; i += i & -i)
                    for (int j = y; j <= c; j += j & -j) bit[i][j] += v;
            } else {
                int x2 = (int) ops[k][3], y2 = (int) ops[k][4];
                long total = sum2(bit, x2, y2) - sum2(bit, x - 1, y2)
                           - sum2(bit, x2, y - 1) + sum2(bit, x - 1, y - 1);
                answer[count++] = total;
            }
        }
        return Arrays.copyOf(answer, count);
    }

    static long sum2(long[][] bit, int x, int y) {
        long s = 0;
        for (int i = x; i > 0; i -= i & -i)
            for (int j = y; j > 0; j -= j & -j) s += bit[i][j];
        return s;
    }
