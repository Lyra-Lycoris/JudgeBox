    static long[] solve(long n, String s, long q, long[][] qs) {
        int m = s.length();
        long[] answer = new long[(int) q];
        Arrays.fill(answer, 1L);
        long[] bases = {131L, 137L};
        long[] mods = {1000000007L, 1000000009L};
        for (int k = 0; k < 2; ++k) {
            long base = bases[k], mod = mods[k];
            long[] power = new long[m + 1];
            power[0] = 1;
            for (int i = 0; i < m; ++i) power[i + 1] = power[i] * base % mod;
            long[] forward = new long[m + 1];
            long[] backward = new long[m + 1];
            for (int i = 0; i < m; ++i) {
                forward[i + 1] = (forward[i] * base + s.charAt(i)) % mod;
                backward[i + 1] = (backward[i] * base + s.charAt(m - 1 - i)) % mod;
            }
            for (int j = 0; j < q; ++j) {
                int left = (int) qs[j][0] - 1;
                int right = (int) qs[j][1];
                int length = right - left;
                long direct = (forward[right] - forward[left] * power[length] % mod + mod) % mod;
                long mirrored = (backward[m - left] - backward[m - right] * power[length] % mod + mod) % mod;
                if (direct != mirrored) answer[j] = 0;
            }
        }
        return answer;
    }
