    static String solve(long n, long k) {
        StringBuilder sb = new StringBuilder((int) n);
        for (long i = 0; i < k; ++i) sb.append('(');
        for (long i = 0; i < k; ++i) sb.append(')');
        for (long i = 0; i < (n - 2 * k) / 2; ++i) sb.append("()");
        return sb.toString();
    }
