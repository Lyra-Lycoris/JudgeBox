    static long solve(long n, long m, long[][] g) {
        int rows = (int) n, cols = (int) m;
        long best = 0;
        long[] heights = new long[cols];
        int[] stack = new int[cols + 1];
        for (int top = 0; top < rows; ++top) {
            Arrays.fill(heights, 0);
            for (int bottom = top; bottom < rows; ++bottom) {
                for (int c = 0; c < cols; ++c) {
                    heights[c] = (g[bottom][c] != 0) ? heights[c] + 1 : 0;
                }
                int sp = 0;
                for (int c = 0; c <= cols; ++c) {
                    long h = (c < cols) ? heights[c] : 0;
                    while (sp > 0 && heights[stack[sp - 1]] >= h) {
                        long ph = heights[stack[sp - 1]];
                        sp--;
                        int left = (sp == 0) ? -1 : stack[sp - 1];
                        long area = ph * (c - left - 1);
                        if (area > best) best = area;
                    }
                    stack[sp++] = c;
                }
            }
        }
        return best;
    }
