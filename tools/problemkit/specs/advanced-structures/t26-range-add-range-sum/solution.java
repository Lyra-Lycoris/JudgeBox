    static long[] solve(long n, long[] a, long q, long[][] ops) {
        int sz = (int) n;
        long[] b1 = new long[sz + 2];
        long[] b2 = new long[sz + 2];
        for (int i = 1; i <= sz; ++i) {
            b1[i] = a[i - 1];
            b2[i] = a[i - 1] * (i - 1);
        }
        for (int i = 1; i <= sz; ++i) {
            int j = i + (i & -i);
            if (j <= sz) {
                b1[j] += b1[i];
                b2[j] += b2[i];
            }
        }

        long[] answer = new long[(int) q];
        int count = 0;
        for (int k = 0; k < (int) q; ++k) {
            long t = ops[k][0], l = ops[k][1], r = ops[k][2], x = ops[k][3];
            if (t == 1) {
                long m1 = x * (l - 1);
                long m2 = x * r;
                for (int i = (int) l; i <= sz; i += i & -i) {
                    b1[i] += x;
                    b2[i] += m1;
                }
                for (int i = (int) r + 1; i <= sz; i += i & -i) {
                    b1[i] -= x;
                    b2[i] -= m2;
                }
            } else {
                long total = 0;
                for (int i = (int) r; i > 0; i -= i & -i) total += b1[i] * r - b2[i];
                for (int i = (int) l - 1; i > 0; i -= i & -i) total -= b1[i] * (l - 1) - b2[i];
                answer[count++] = total;
            }
        }
        return Arrays.copyOf(answer, count);
    }
