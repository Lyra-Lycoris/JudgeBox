    static long[] solve(long n, long[] ids, long[] chinese, long[] math, long[] english) {
        long[][] rows = new long[(int) n][3];
        for (int i = 0; i < n; ++i) {
            rows[i][0] = chinese[i] + math[i] + english[i];
            rows[i][1] = chinese[i];
            rows[i][2] = ids[i];
        }
        Arrays.sort(rows, (a, b) -> {
            if (a[0] != b[0]) return Long.compare(b[0], a[0]);
            if (a[1] != b[1]) return Long.compare(b[1], a[1]);
            return Long.compare(a[2], b[2]);
        });
        long[] answer = new long[(int) n];
        for (int i = 0; i < n; ++i) answer[i] = rows[i][2];
        return answer;
    }
