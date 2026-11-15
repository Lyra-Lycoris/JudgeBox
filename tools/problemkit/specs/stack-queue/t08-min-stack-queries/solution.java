    static long[] solve(long m, long[] op, long[] val) {
        int size = (int) m;
        long[] stack = new long[size];
        long[] minimum = new long[size];
        long[] answer = new long[size];
        int top = 0;
        int count = 0;
        for (int i = 0; i < size; ++i) {
            if (op[i] == 1) {
                long v = val[i];
                stack[top] = v;
                minimum[top] = top == 0 ? v : Math.min(minimum[top - 1], v);
                top += 1;
            } else if (op[i] == 2) {
                top -= 1;
            } else {
                answer[count++] = minimum[top - 1];
            }
        }
        long[] result = new long[count];
        System.arraycopy(answer, 0, result, 0, count);
        return result;
    }
