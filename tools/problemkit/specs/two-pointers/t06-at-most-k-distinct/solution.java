    static long solve(long k, String s) {
        if (k <= 0 || s.isEmpty()) return 0;
        long[] count = new long[256];
        long distinct = 0, best = 0;
        int left = 0;
        for (int right = 0; right < s.length(); ++right) {
            int c = s.charAt(right);
            if (count[c] == 0) distinct++;
            count[c]++;
            while (distinct > k) {
                int d = s.charAt(left);
                count[d]--;
                if (count[d] == 0) distinct--;
                left++;
            }
            if (right - left + 1 > best) best = right - left + 1;
        }
        return best;
    }
