    static long solve(long n, long cap, long[] g, long[] w, long[] v) {
        ArrayList<ArrayList<Integer>> groups = new ArrayList<>();
        for (int i = 0; i <= n + 1; ++i) groups.add(new ArrayList<Integer>());
        for (int i = 0; i < n; ++i) groups.get((int) g[i]).add(i);
        long[] dp = new long[(int) cap + 1];
        for (int key = 1; key <= n; ++key) {
            if (groups.get(key).isEmpty()) continue;
            long[] ndp = dp.clone();
            for (int idx : groups.get(key)) {
                if (w[idx] > cap) continue;
                for (long j = cap; j >= w[idx]; --j) {
                    long cand = dp[(int) (j - w[idx])] + v[idx];
                    if (cand > ndp[(int) j]) ndp[(int) j] = cand;
                }
            }
            dp = ndp;
        }
        return dp[(int) cap];
    }
