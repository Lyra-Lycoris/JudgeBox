    static long solve(long n, long cost, long[] a) {
        int N = (int) n;
        long[] S = new long[N + 1];
        for (int i = 1; i <= N; ++i) S[i] = S[i - 1] + a[i - 1];
        long[] ms = new long[N + 2];
        long[] bs = new long[N + 2];
        int head = 0, tail = 1;
        long answer = 0;
        for (int i = 1; i <= N; ++i) {
            long si = S[i];
            long x = -2 * si;
            while (head + 1 < tail && ms[head + 1] * x + bs[head + 1] <= ms[head] * x + bs[head]) {
                ++head;
            }
            long best = ms[head] * x + bs[head];
            long dpi = best + si * si + cost;
            if (i == N) answer = dpi;
            long m = si, b = dpi + si * si;
            while (tail - head >= 2) {
                long m1 = ms[tail - 2], b1 = bs[tail - 2];
                long m2 = ms[tail - 1], b2 = bs[tail - 1];
                BigInteger left = BigInteger.valueOf(b2 - b1).multiply(BigInteger.valueOf(m - m2));
                BigInteger right = BigInteger.valueOf(b - b2).multiply(BigInteger.valueOf(m2 - m1));
                if (left.compareTo(right) >= 0) {
                    --tail;
                } else {
                    break;
                }
            }
            ms[tail] = m;
            bs[tail] = b;
            ++tail;
        }
        return answer;
    }
