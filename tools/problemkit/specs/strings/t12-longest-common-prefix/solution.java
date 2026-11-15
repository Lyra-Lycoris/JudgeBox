    static long solve(long k, String[] words) {
        int limit = words[0].length();
        for (String w : words) limit = Math.min(limit, w.length());
        int i = 0;
        while (i < limit) {
            char ch = words[0].charAt(i);
            boolean ok = true;
            for (String w : words) {
                if (w.charAt(i) != ch) {
                    ok = false;
                    break;
                }
            }
            if (!ok) break;
            ++i;
        }
        return i;
    }
