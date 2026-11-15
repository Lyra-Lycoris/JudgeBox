    static long solve(long n, String begin, String end, String[] w) {
        int N = (int) n;
        if (begin.equals(end)) return 1;
        int target = -1, bidx = -1;
        for (int i = 0; i < N; ++i) {
            if (target < 0 && w[i].equals(end)) target = i;
            if (bidx < 0 && w[i].equals(begin)) bidx = i;
        }
        if (target < 0) return 0;

        HashMap<String, ArrayList<Integer>> buckets = new HashMap<>();
        for (int i = 0; i < N; ++i) {
            char[] chars = w[i].toCharArray();
            for (int j = 0; j < chars.length; ++j) {
                char old = chars[j];
                chars[j] = '*';
                String key = new String(chars);
                chars[j] = old;
                ArrayList<Integer> group = buckets.get(key);
                if (group == null) {
                    group = new ArrayList<>();
                    buckets.put(key, group);
                }
                group.add(i);
            }
        }

        long[] dist = new long[N + 1];
        Arrays.fill(dist, -1);
        dist[N] = 1;
        if (bidx >= 0) dist[bidx] = 1;
        int[] queue = new int[N + 1];
        int head = 0, tail = 0;
        queue[tail++] = N;
        while (head < tail) {
            int u = queue[head++];
            long step = dist[u] + 1;
            String word = (u == N) ? begin : w[u];
            char[] chars = word.toCharArray();
            for (int j = 0; j < chars.length; ++j) {
                char old = chars[j];
                chars[j] = '*';
                String key = new String(chars);
                chars[j] = old;
                ArrayList<Integer> group = buckets.remove(key);
                if (group == null) continue;
                for (int idx = 0; idx < group.size(); ++idx) {
                    int v = group.get(idx);
                    if (dist[v] != -1) continue;
                    dist[v] = step;
                    if (v == target) return step;
                    queue[tail++] = v;
                }
            }
        }
        return 0;
    }
