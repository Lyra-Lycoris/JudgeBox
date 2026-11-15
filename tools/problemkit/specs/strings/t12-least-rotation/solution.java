    static long solve(long n, String s) {
        int m = s.length();
        if (m <= 1) return 0;
        String doubled = s + s;
        int i = 0, j = 1, k = 0;
        while (i < m && j < m && k < m) {
            char a = doubled.charAt(i + k);
            char b = doubled.charAt(j + k);
            if (a == b) {
                ++k;
            } else if (a > b) {
                i = i + k + 1;
                if (i <= j) i = j + 1;
                k = 0;
            } else {
                j = j + k + 1;
                if (j <= i) j = i + 1;
                k = 0;
            }
        }
        return Math.min(i, j);
    }
