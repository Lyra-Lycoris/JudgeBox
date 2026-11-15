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

    static long solve(long n) {
        final long MOD = 1000000007L;
        long answer = (powMod(2, n + 1) - 2) % MOD;
        if (answer < 0) answer += MOD;
        return answer;
    }
