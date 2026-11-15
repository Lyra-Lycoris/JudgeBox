    static boolean solve(String s) {
        char[] stack = new char[s.length() + 1];
        int top = 0;
        for (int i = 0; i < s.length(); ++i) {
            char c = s.charAt(i);
            if (c == '(') {
                stack[top++] = ')';
            } else if (c == '[') {
                stack[top++] = ']';
            } else if (c == '{') {
                stack[top++] = '}';
            } else {
                if (top == 0 || stack[top - 1] != c) return false;
                top -= 1;
            }
        }
        return top == 0;
    }
