    static String solve(long k, String s) {
        char[] chars = new char[s.length() + 1];
        int[] counts = new int[s.length() + 1];
        int top = 0;
        for (int i = 0; i < s.length(); ++i) {
            char c = s.charAt(i);
            if (top > 0 && chars[top - 1] == c) {
                counts[top - 1] += 1;
                if (counts[top - 1] == k) top -= 1;
            } else {
                chars[top] = c;
                counts[top] = 1;
                top += 1;
            }
        }
        StringBuilder answer = new StringBuilder();
        for (int i = 0; i < top; ++i) {
            for (int j = 0; j < counts[i]; ++j) answer.append(chars[i]);
        }
        return answer.toString();
    }
