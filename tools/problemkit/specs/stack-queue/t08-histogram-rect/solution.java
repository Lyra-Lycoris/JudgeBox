    static long solve(long n, long[] h) {
        int size = (int) n;
        int[] stack = new int[size + 1];
        int top = 0;
        long best = 0;
        for (int i = 0; i <= size; ++i) {
            long cur = i < size ? h[i] : 0;
            while (top > 0 && h[stack[top - 1]] >= cur) {
                long height = h[stack[--top]];
                int left = top > 0 ? stack[top - 1] : -1;
                long area = height * (i - left - 1);
                if (area > best) best = area;
            }
            stack[top++] = i;
        }
        return best;
    }
