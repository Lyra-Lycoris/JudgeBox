    static long solve(String s, String t) {
        int n = s.length();
        int m = t.length();
        int[] prev = new int[m + 1];
        int[] cur = new int[m + 1];
        for (int i = 0; i < n; ++i) {
            char c = s.charAt(i);
            for (int j = 1; j <= m; ++j) {
                if (c == t.charAt(j - 1)) cur[j] = prev[j - 1] + 1;
                else cur[j] = Math.max(prev[j], cur[j - 1]);
            }
            int[] tmp = prev;
            prev = cur;
            cur = tmp;
        }
        return prev[m];
    }
