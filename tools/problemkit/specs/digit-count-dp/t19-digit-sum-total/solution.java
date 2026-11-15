    static long solve(long l, long r) {
        return totalUpTo(r) - totalUpTo(l - 1);
    }

    static long totalUpTo(long x) {
        if (x < 0) return 0;
        long[] power = new long[17];
        power[0] = 1;
        for (int i = 1; i < 17; ++i) power[i] = power[i - 1] * 10;
        long[] suffix = new long[17];
        suffix[0] = 0;
        for (int i = 1; i < 17; ++i) suffix[i] = (long) i * 45 * power[i - 1];

        int[] digits = new int[20];
        int len = 0;
        long t = x;
        while (true) {
            digits[len++] = (int) (t % 10);
            t /= 10;
            if (t == 0) break;
        }
        long result = 0;
        long prefix = 0;
        for (int pos = len - 1; pos >= 0; --pos) {
            int cur = digits[pos];
            for (int v = 0; v < cur; ++v) {
                result += (prefix + v) * power[pos] + suffix[pos];
            }
            prefix += cur;
        }
        return result + prefix;
    }
