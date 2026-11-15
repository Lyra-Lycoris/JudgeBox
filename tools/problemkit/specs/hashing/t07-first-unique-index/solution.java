    static long solve(long n, String s) {
        int[] counts = new int[26];
        for (int i = 0; i < s.length(); ++i) counts[s.charAt(i) - 'a'] += 1;
        for (int i = 0; i < s.length(); ++i) {
            if (counts[s.charAt(i) - 'a'] == 1) return i + 1;
        }
        return -1;
    }
