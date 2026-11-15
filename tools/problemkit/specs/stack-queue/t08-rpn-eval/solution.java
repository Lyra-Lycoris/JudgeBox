    static long solve(long k, String[] tokens) {
        long[] stack = new long[(int) (k / 2 + 2)];
        int top = 0;
        for (String token : tokens) {
            if (token.length() == 1 && "+-*/".indexOf(token.charAt(0)) >= 0) {
                long b = stack[--top];
                long a = stack[--top];
                char op = token.charAt(0);
                long result;
                if (op == '+') {
                    result = a + b;
                } else if (op == '-') {
                    result = a - b;
                } else if (op == '*') {
                    result = a * b;
                } else {
                    result = a / b;
                }
                stack[top++] = result;
            } else {
                stack[top++] = Long.parseLong(token);
            }
        }
        return stack[top - 1];
    }
