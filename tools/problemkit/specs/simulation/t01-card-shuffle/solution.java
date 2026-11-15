    static long[] solve(long n, long k, long[] p) {
        int total = (int) n;
        int[] perm = new int[total];
        for (int i = 0; i < total; ++i) perm[i] = (int) p[i] - 1;
        long[] answer = new long[total];
        boolean[] visited = new boolean[total];
        int[] cycle = new int[total];
        for (int start = 0; start < total; ++start) {
            if (visited[start]) continue;
            int length = 0;
            int current = start;
            while (!visited[current]) {
                visited[current] = true;
                cycle[length++] = current;
                current = perm[current];
            }
            long shift = k % length;
            for (int j = 0; j < length; ++j) {
                long source = ((j - shift) % length + length) % length;
                answer[cycle[j]] = cycle[(int) source] + 1L;
            }
        }
        return answer;
    }
