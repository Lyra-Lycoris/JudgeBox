    static long solve(long n, String s) {
        final long MOD = 1000000007L;
        int length = (int) Math.min(n, (long) s.length());
        if (length <= 0) return 0;
        long[] dp = new long[length + 1];
        long[] last = new long[26];
        for (int i = 0; i < 26; ++i) last[i] = -1;
        dp[0] = 1;
        for (int i = 1; i <= length; ++i) {
            int c = s.charAt(i - 1) - 'a';
            long value = 2 * dp[i - 1] % MOD;
            if (last[c] >= 0) value = (value - dp[(int) last[c]] + MOD) % MOD;
            dp[i] = value;
            last[c] = i - 1;
        }
        return (dp[length] - 1 + MOD) % MOD;
    }
