    static long solve(long l, long r) {
        return countNoFour(r) - countNoFour(l - 1);
    }

    static long countNoFour(long x) {
        if (x < 0) return 0;
        int[] digits = new int[20];
        int len = 0;
        long t = x;
        while (true) {
            digits[len++] = (int) (t % 10);
            t /= 10;
            if (t == 0) break;
        }
        long[] power = new long[21];
        power[0] = 1;
        for (int i = 1; i <= len; ++i) power[i] = power[i - 1] * 9;
        long total = 0;
        for (int pos = len - 1; pos >= 0; --pos) {
            int cur = digits[pos];
            long smaller = 0;
            for (int v = 0; v < cur; ++v) {
                if (v != 4) ++smaller;
            }
            total += smaller * power[pos];
            if (cur == 4) return total;
        }
        return total + 1;
    }
