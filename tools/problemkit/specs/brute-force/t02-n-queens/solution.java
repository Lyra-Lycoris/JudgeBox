    static long nqDfs(int row, int n, boolean[] col, boolean[] d1, boolean[] d2) {
        if (row == n) return 1;
        long total = 0;
        for (int c = 0; c < n; ++c) {
            int a = row + c;
            int b = row - c + n;
            if (col[c] || d1[a] || d2[b]) continue;
            col[c] = d1[a] = d2[b] = true;
            total += nqDfs(row + 1, n, col, d1, d2);
            col[c] = d1[a] = d2[b] = false;
        }
        return total;
    }

    static long solve(long n) {
        int len = (int) n;
        boolean[] col = new boolean[len];
        boolean[] d1 = new boolean[2 * len];
        boolean[] d2 = new boolean[2 * len];
        return nqDfs(0, len, col, d1, d2);
    }
