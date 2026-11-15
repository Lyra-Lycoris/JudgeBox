    static long solve(String s) {
        int n = s.length();
        long[] counts = new long[2 * n + 1];
        int[] stack = new int[n + 1];
        int top = 0;
        long prefix = 0;
        long answer = 0;
        counts[n] = 1;
        stack[0] = 0;
        top = 1;
        for (int k = 0; k < n; ++k) {
            prefix += (s.charAt(k) == '(') ? 1 : -1;
            while (top > 0 && stack[top - 1] > prefix) {
                counts[stack[top - 1] + n] = 0;
                --top;
            }
            answer += counts[(int) prefix + n];
            counts[(int) prefix + n] += 1;
            if (top == 0 || stack[top - 1] < prefix) {
                stack[top] = (int) prefix;
                ++top;
            }
        }
        return answer;
    }
