    static long[] solve(long n, long k, long[] guesses, long[] exact, long[] loose) {
        int len = (int) n;
        int cnt = (int) k;
        int[][] gd = new int[cnt][len];
        for (int q = 0; q < cnt; ++q) {
            long v = guesses[q];
            for (int i = len - 1; i >= 0; --i) {
                gd[q][i] = (int) (v % 10);
                v /= 10;
            }
        }
        long total = 1;
        for (int i = 0; i < len; ++i) total *= 10;
        int[] cd = new int[len];
        for (long code = 0; code < total; ++code) {
            long t = code;
            for (int i = len - 1; i >= 0; --i) {
                cd[i] = (int) (t % 10);
                t /= 10;
            }
            boolean ok = true;
            for (int q = 0; q < cnt && ok; ++q) {
                int a = 0, b = 0;
                int[] ca = new int[10];
                int[] cb = new int[10];
                for (int i = 0; i < len; ++i) {
                    if (cd[i] == gd[q][i]) ++a;
                    ++ca[cd[i]];
                    ++cb[gd[q][i]];
                }
                for (int d = 0; d < 10; ++d) b += Math.min(ca[d], cb[d]);
                b -= a;
                if (a != exact[q] || b != loose[q]) ok = false;
            }
            if (ok) {
                long[] answer = new long[len];
                for (int i = 0; i < len; ++i) answer[i] = cd[i];
                return answer;
            }
        }
        long[] answer = new long[len];
        for (int i = 0; i < len; ++i) answer[i] = cd[i];
        return answer;
    }
