    static long solve(String s) {
        int n = s.length();
        if (n <= 1) return 0;
        int[] dp = new int[n + 1];
        Arrays.fill(dp, n + 1);
        dp[0] = 0;
        for (int c = 0; c < n; ++c) {
            for (int l = c, r = c; l >= 0 && r < n && s.charAt(l) == s.charAt(r); --l, ++r) {
                if (dp[l] + 1 < dp[r + 1]) dp[r + 1] = dp[l] + 1;
            }
            for (int l = c, r = c + 1; l >= 0 && r < n && s.charAt(l) == s.charAt(r); --l, ++r) {
                if (dp[l] + 1 < dp[r + 1]) dp[r + 1] = dp[l] + 1;
            }
        }
        return dp[n] - 1;
    }
