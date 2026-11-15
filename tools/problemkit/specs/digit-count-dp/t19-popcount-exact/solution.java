    static long solve(long l, long r, long k) {
        long[][] comb = new long[62][62];
        for (int i = 0; i < 62; ++i) {
            comb[i][0] = 1;
            for (int j = 1; j <= i; ++j) comb[i][j] = comb[i - 1][j - 1] + comb[i - 1][j];
        }
        return countUpTo(r, k, comb) - countUpTo(l - 1, k, comb);
    }

    static long countUpTo(long x, long k, long[][] comb) {
        if (x < 0 || k < 0) return 0;
        long res = 0;
        long used = 0;
        boolean ok = true;
        for (int bit = 60; bit >= 0; --bit) {
            if (((x >> bit) & 1L) != 0L) {
                long need = k - used;
                if (need >= 0 && need <= bit) res += comb[bit][(int) need];
                used += 1;
                if (used > k) {
                    ok = false;
                    break;
                }
            }
        }
        if (ok && used == k) res += 1;
        return res;
    }
