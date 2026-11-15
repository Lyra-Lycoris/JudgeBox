    static long solve(String s) {
        long[] last = new long[256];
        for (int i = 0; i < 256; ++i) last[i] = -1;
        long best = 0, left = 0;
        for (int right = 0; right < s.length(); ++right) {
            int c = s.charAt(right);
            if (last[c] >= left) left = last[c] + 1;
            last[c] = right;
            if (right - left + 1 > best) best = right - left + 1;
        }
        return best;
    }
