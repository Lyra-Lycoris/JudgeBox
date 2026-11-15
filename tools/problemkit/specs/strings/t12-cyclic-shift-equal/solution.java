    static boolean solve(long n, String s, String t) {
        if (s.length() != t.length()) return false;
        int m = s.length();
        String doubled = s + s;
        long[] bases = {131L, 137L};
        long[] mods = {1000000007L, 1000000009L};
        for (int k = 0; k < 2; ++k) {
            long base = bases[k], mod = mods[k];
            long power = 1;
            for (int i = 0; i < m; ++i) power = power * base % mod;
            long target = 0;
            for (int i = 0; i < m; ++i) target = (target * base + t.charAt(i)) % mod;
            long[] prefix = new long[2 * m + 1];
            for (int i = 0; i < 2 * m; ++i) prefix[i + 1] = (prefix[i] * base + doubled.charAt(i)) % mod;
            boolean matched = false;
            for (int i = 0; i < m; ++i) {
                long value = (prefix[i + m] - prefix[i] * power % mod + mod) % mod;
                if (value == target) {
                    matched = true;
                    break;
                }
            }
            if (!matched) return false;
        }
        return true;
    }
