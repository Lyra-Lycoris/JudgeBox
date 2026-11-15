    static long powMod(long base, long exp) {
        final long MOD = 1000000007L;
        long result = 1;
        base %= MOD;
        while (exp > 0) {
            if ((exp & 1L) == 1L) result = result * base % MOD;
            base = base * base % MOD;
            exp >>= 1;
        }
        return result;
    }

    static long norm(long value) {
        final long MOD = 1000000007L;
        long r = value % MOD;
        if (r < 0) r += MOD;
        return r;
    }

    static long solve(long n, long[] a) {
        final long MOD = 1000000007L;
        if (n < 2) return 0;

        int len = (int) n;
        long[] uniq = new long[len];
        System.arraycopy(a, 0, uniq, 0, len);
        Arrays.sort(uniq);
        int m = 0;
        for (int i = 0; i < len; ++i) {
            if (i == 0 || uniq[i] != uniq[i - 1]) uniq[m++] = uniq[i];
        }

        long[] cnt = new long[m];
        long[] lessCnt = new long[m];
        long[] greaterCnt = new long[m];
        for (int i = 0; i < len; ++i) {
            int idx = Arrays.binarySearch(uniq, 0, m, a[i]);
            cnt[idx]++;
        }
        long running = 0;
        for (int i = 0; i < m; ++i) {
            lessCnt[i] = running;
            running += cnt[i];
        }
        for (int i = 0; i < m; ++i) {
            greaterCnt[i] = n - lessCnt[i] - cnt[i];
        }

        long[] tree = new long[m + 1];
        long invCount = 0;
        for (int k = 0; k < len; ++k) {
            int r = Arrays.binarySearch(uniq, 0, m, a[k]) + 1;
            long seen = 0;
            for (int i = r; i > 0; i -= i & -i) seen += tree[i];
            invCount += k - seen;
            for (int i = r; i <= m; i += i & -i) tree[i]++;
        }

        long equalPairs = 0;
        for (int i = 0; i < m; ++i) equalPairs += cnt[i] * (cnt[i] - 1) / 2;
        long totalPairs = n * (n - 1) / 2;
        long untouched = (n - 2) * (n - 3) / 2;

        long total = norm((untouched % MOD) * (invCount % MOD));
        total = norm(total + norm((totalPairs % MOD) - (invCount % MOD) - (equalPairs % MOD)));

        long sumLeft = 0;
        for (int k = 0; k < len; ++k) {
            int idx = Arrays.binarySearch(uniq, 0, m, a[k]);
            sumLeft = norm(sumLeft + norm((k % MOD) * (greaterCnt[idx] % MOD)));
        }
        total = norm(total + sumLeft);

        long sumRight = 0;
        for (int k = 0; k < len; ++k) {
            int idx = Arrays.binarySearch(uniq, 0, m, a[k]);
            sumRight = norm(sumRight + norm(((n - 1 - k) % MOD) * (lessCnt[idx] % MOD)));
        }
        total = norm(total + sumRight);

        total = norm(total - 2 * (invCount % MOD) % MOD);
        return norm(total * powMod(totalPairs % MOD, MOD - 2));
    }
