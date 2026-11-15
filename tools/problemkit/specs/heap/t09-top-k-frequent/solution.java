    static long[] solve(long n, long k, long[] a) {
        HashMap<Long, Long> count = new HashMap<Long, Long>();
        for (long x : a) {
            Long cur = count.get(x);
            count.put(x, cur == null ? 1L : cur + 1);
        }
        long[][] items = new long[count.size()][2];
        int pos = 0;
        for (Map.Entry<Long, Long> entry : count.entrySet()) {
            items[pos][0] = -entry.getValue();
            items[pos][1] = entry.getKey();
            pos++;
        }
        Arrays.sort(items, new Comparator<long[]>() {
            public int compare(long[] x, long[] y) {
                if (x[0] != y[0]) return Long.compare(x[0], y[0]);
                return Long.compare(x[1], y[1]);
            }
        });
        long[] answer = new long[(int) k];
        for (int i = 0; i < (int) k; ++i) answer[i] = items[i][1];
        return answer;
    }
