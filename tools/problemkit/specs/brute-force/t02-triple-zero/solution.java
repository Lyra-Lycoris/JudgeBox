    static long solve(long n, long[] a) {
        long[] v = a.clone();
        Arrays.sort(v);
        int len = (int) n;
        long total = 0;
        for (int i = 0; i + 2 < len; ++i) {
            int l = i + 1, r = len - 1;
            while (l < r) {
                long s = v[i] + v[l] + v[r];
                if (s == 0) {
                    if (v[l] == v[r]) {
                        long c = r - l + 1;
                        total += c * (c - 1) / 2;
                        break;
                    }
                    int cl = 1, cr = 1;
                    while (l + cl < r && v[l + cl] == v[l]) ++cl;
                    while (r - cr > l && v[r - cr] == v[r]) ++cr;
                    total += (long) cl * cr;
                    l += cl;
                    r -= cr;
                } else if (s < 0) {
                    ++l;
                } else {
                    --r;
                }
            }
        }
        return total;
    }
