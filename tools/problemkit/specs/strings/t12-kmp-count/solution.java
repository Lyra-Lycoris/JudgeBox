    static long solve(long n, String s, long m, String p) {
        if (m <= 0 || s.length() < m) return 0;
        int[] pi = new int[(int) m];
        for (int i = 1; i < m; ++i) {
            int k = pi[i - 1];
            while (k > 0 && p.charAt(i) != p.charAt(k)) k = pi[k - 1];
            if (p.charAt(i) == p.charAt(k)) ++k;
            pi[i] = k;
        }
        long count = 0;
        int k = 0;
        for (int i = 0; i < s.length(); ++i) {
            char ch = s.charAt(i);
            while (k > 0 && ch != p.charAt(k)) k = pi[k - 1];
            if (ch == p.charAt(k)) {
                ++k;
                if (k == m) {
                    ++count;
                    k = pi[k - 1];
                }
            }
        }
        return count;
    }
