    static long solve(long k, long[] v, long[] c) {
        long cand = 0, balance = 0;
        for (int i = 0; i < k; ++i) {
            long cnt = c[i];
            if (balance == 0) {
                cand = v[i];
                balance = cnt;
            } else if (v[i] == cand) {
                balance += cnt;
            } else if (cnt < balance) {
                balance -= cnt;
            } else {
                cand = v[i];
                balance = cnt - balance;
            }
        }
        return cand;
    }
