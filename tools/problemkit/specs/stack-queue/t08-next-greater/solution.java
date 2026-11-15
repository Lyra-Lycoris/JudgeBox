    static long[] solve(long n, long[] a) {
        int size = (int) n;
        long[] answer = new long[size];
        long[] stack = new long[size];
        int top = 0;
        for (int i = size - 1; i >= 0; --i) {
            while (top > 0 && stack[top - 1] <= a[i]) top -= 1;
            answer[i] = top > 0 ? stack[top - 1] : -1L;
            stack[top++] = a[i];
        }
        return answer;
    }
