    static long solve(long n) {
        if (n < 10) return n;
        String s = Long.toString(n);
        int L = s.length();
        String half = s.substring(0, (L + 1) / 2);

        StringBuilder back = new StringBuilder(half.substring(0, L / 2));
        long candidate = Long.parseLong(half + back.reverse().toString());
        if (candidate >= n) return candidate;

        char[] digits = half.toCharArray();
        int i = digits.length - 1;
        while (i >= 0 && digits[i] == '9') {
            digits[i] = '0';
            --i;
        }
        if (i < 0) {
            StringBuilder answer = new StringBuilder("1");
            for (int k = 0; k < L - 1; ++k) answer.append('0');
            answer.append('1');
            return Long.parseLong(answer.toString());
        }
        digits[i] += 1;

        String next = new String(digits);
        StringBuilder back2 = new StringBuilder(next.substring(0, L / 2));
        return Long.parseLong(next + back2.reverse().toString());
    }
