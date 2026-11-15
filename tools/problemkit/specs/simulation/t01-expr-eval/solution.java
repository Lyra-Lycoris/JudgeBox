    static int precedenceOf(char op) {
        return (op == '*' || op == '/') ? 2 : 1;
    }

    static void applyTop(long[] values, int[] valueTop, char[] ops, int[] opTop) {
        char op = ops[--opTop[0]];
        long b = values[--valueTop[0]];
        long a = values[--valueTop[0]];
        long result = 0;
        if (op == '+') {
            result = a + b;
        } else if (op == '-') {
            result = a - b;
        } else if (op == '*') {
            result = a * b;
        } else {
            long quotient = Math.abs(a) / Math.abs(b);
            result = ((a < 0) == (b < 0)) ? quotient : -quotient;
        }
        values[valueTop[0]++] = result;
    }

    static long solve(String expr) {
        int length = expr.length();
        long[] values = new long[length + 2];
        char[] ops = new char[length + 2];
        int[] valueTop = {0};
        int[] opTop = {0};
        int index = 0;
        while (index < length) {
            char ch = expr.charAt(index);
            if (ch >= '0' && ch <= '9') {
                long number = 0;
                while (index < length && expr.charAt(index) >= '0' && expr.charAt(index) <= '9') {
                    number = number * 10 + (expr.charAt(index) - '0');
                    index++;
                }
                values[valueTop[0]++] = number;
                continue;
            }
            if (ch == '(') {
                ops[opTop[0]++] = ch;
            } else if (ch == ')') {
                while (ops[opTop[0] - 1] != '(') applyTop(values, valueTop, ops, opTop);
                opTop[0]--;
            } else {
                while (opTop[0] > 0 && ops[opTop[0] - 1] != '('
                        && precedenceOf(ops[opTop[0] - 1]) >= precedenceOf(ch)) {
                    applyTop(values, valueTop, ops, opTop);
                }
                ops[opTop[0]++] = ch;
            }
            index++;
        }
        while (opTop[0] > 0) applyTop(values, valueTop, ops, opTop);
        return values[0];
    }
