    static long solve(String s, String t) {
        int n = s.length();
        int m = t.length();
        int[] prev = new int[m + 1];
        int[] cur = new int[m + 1];
        for (int j = 0; j <= m; ++j) prev[j] = j;
        for (int i = 1; i <= n; ++i) {
            cur[0] = i;
            char c = s.charAt(i - 1);
            for (int j = 1; j <= m; ++j) {
                int best = Math.min(prev[j] + 1, cur[j - 1] + 1);
                int sub = prev[j - 1] + (c == t.charAt(j - 1) ? 0 : 1);
                if (sub < best) best = sub;
                cur[j] = best;
            }
            int[] tmp = prev;
            prev = cur;
            cur = tmp;
        }
        return prev[m];
    }
