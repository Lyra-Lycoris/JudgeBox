    static long solve(long n, String s) {
        int m = s.length();
        if (m <= 0) return 0;
        int[] pi = new int[m];
        for (int i = 1; i < m; ++i) {
            int k = pi[i - 1];
            while (k > 0 && s.charAt(i) != s.charAt(k)) k = pi[k - 1];
            if (s.charAt(i) == s.charAt(k)) ++k;
            pi[i] = k;
        }
        long d = m - pi[m - 1];
        return (m % d == 0) ? d : m;
    }
