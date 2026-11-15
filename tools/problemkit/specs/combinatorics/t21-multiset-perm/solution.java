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

    static long solve(long n, long[] a) {
        final long MOD = 1000000007L;
        Arrays.sort(a);
        int m = (int) n;
        long[] fact = new long[m + 1];
        long[] invfact = new long[m + 1];
        fact[0] = 1;
        for (int i = 1; i <= m; ++i) fact[i] = fact[i - 1] * i % MOD;
        invfact[m] = powMod(fact[m], MOD - 2);
        for (int i = m; i >= 1; --i) invfact[i - 1] = invfact[i] * i % MOD;
        long answer = fact[m];
        int i = 0;
        while (i < m) {
            int j = i + 1;
            while (j < m && a[j] == a[i]) ++j;
            answer = answer * invfact[j - i] % MOD;
            i = j;
        }
        return answer;
    }
