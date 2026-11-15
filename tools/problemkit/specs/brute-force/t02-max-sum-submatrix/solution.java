    static long solve(long n, long m, long[][] g) {
        int rows = (int) n, cols = (int) m;
        long answer = g[0][0];
        long[] sums = new long[cols];
        for (int top = 0; top < rows; ++top) {
            Arrays.fill(sums, 0);
            for (int bottom = top; bottom < rows; ++bottom) {
                for (int c = 0; c < cols; ++c) sums[c] += g[bottom][c];
                long cur = sums[0], best = sums[0];
                for (int c = 1; c < cols; ++c) {
                    cur = Math.max(sums[c], cur + sums[c]);
                    best = Math.max(best, cur);
                }
                answer = Math.max(answer, best);
            }
        }
        return answer;
    }
