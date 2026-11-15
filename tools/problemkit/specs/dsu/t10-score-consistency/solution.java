    // diff[x] = value[x] - value[parent[x]]
    static int find(int[] parent, long[] diff, int x) {
        int root = x;
        long total = 0;
        while (parent[root] != root) {
            total += diff[root];
            root = parent[root];
        }
        int cur = x;
        long remain = total;
        while (parent[cur] != cur) {
            int nxt = parent[cur];
            long old = diff[cur];
            parent[cur] = root;
            diff[cur] = remain;
            remain -= old;
            cur = nxt;
        }
        return root;
    }

    static boolean solve(long n, long k, long[][] rel) {
        int nn = (int) n;
        int[] parent = new int[nn + 1];
        int[] size = new int[nn + 1];
        long[] diff = new long[nn + 1];
        for (int i = 0; i <= nn; ++i) {
            parent[i] = i;
            size[i] = 1;
        }
        int kk = (int) k;
        for (int i = 0; i < kk; ++i) {
            int a = (int) rel[i][0];
            int b = (int) rel[i][1];
            long c = rel[i][2];
            int ra = find(parent, diff, a);
            long da = diff[a];
            int rb = find(parent, diff, b);
            long db = diff[b];
            if (ra == rb) {
                if (da - db != c) return false;
                continue;
            }
            if (size[ra] < size[rb]) {
                parent[ra] = rb;
                diff[ra] = -(da - db - c);
                size[rb] += size[ra];
            } else {
                parent[rb] = ra;
                diff[rb] = da - db - c;
                size[ra] += size[rb];
            }
        }
        return true;
    }
