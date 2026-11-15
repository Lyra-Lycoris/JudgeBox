    static long solve(long n, long[] a) {
        int len = (int) n;
        long[] keys = new long[len];
        for (int i = 0; i < len; ++i) {
            keys[i] = (a[i] + 1000000000L) * 1000000L + i;
        }
        java.util.Arrays.sort(keys);
        long[] bit = new long[len + 1];
        long answer = 0;
        long seen = 0;
        for (int k = 0; k < len; ++k) {
            int pos = (int) (keys[k] % 1000000L) + 1;
            long s = 0;
            for (int t = pos; t > 0; t -= t & (-t)) s += bit[t];
            answer += seen - s;
            ++seen;
            for (int t = pos; t <= len; t += t & (-t)) ++bit[t];
        }
        return answer;
    }
