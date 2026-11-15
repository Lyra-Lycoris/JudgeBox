    static String solve(String a, String b) {
        int i = a.length() - 1;
        int j = b.length() - 1;
        int carry = 0;
        StringBuilder sb = new StringBuilder();
        while (i >= 0 || j >= 0 || carry > 0) {
            int total = carry;
            if (i >= 0) {
                total += a.charAt(i) - '0';
                --i;
            }
            if (j >= 0) {
                total += b.charAt(j) - '0';
                --j;
            }
            sb.append((char) ('0' + total % 10));
            carry = total / 10;
        }
        return sb.reverse().toString();
    }
