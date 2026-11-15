    static long solve(long l, long r, long k) {
        long[][] cnt = new long[19][10];
        for (int last = 0; last < 10; ++last) cnt[0][last] = 1;
        for (int rem = 1; rem < 19; ++rem) {
            for (int last = 0; last < 10; ++last) {
                long sum = 0;
                for (int v = 0; v < 10; ++v) {
                    if (Math.abs(v - last) <= k) sum += cnt[rem - 1][v];
                }
                cnt[rem][last] = sum;
            }
        }
        return countUpTo(r, k, cnt) - countUpTo(l - 1, k, cnt);
    }

    static long countUpTo(long x, long k, long[][] cnt) {
        if (x <= 0) return 0;
        int[] digits = new int[20];
        int len = 0;
        long t = x;
        while (true) {
            digits[len++] = (int) (t % 10);
            t /= 10;
            if (t == 0) break;
        }
        long res = 0;
        for (int length = 1; length < len; ++length) {
            for (int first = 1; first <= 9; ++first) res += cnt[length - 1][first];
        }
        for (int pos = len - 1; pos >= 0; --pos) {
            int lo = (pos == len - 1) ? 1 : 0;
            for (int v = lo; v < digits[pos]; ++v) {
                if (pos < len - 1 && Math.abs(v - digits[pos + 1]) > k) continue;
                res += cnt[pos][v];
            }
            if (pos < len - 1 && Math.abs(digits[pos] - digits[pos + 1]) > k) return res;
        }
        return res + 1;
    }
