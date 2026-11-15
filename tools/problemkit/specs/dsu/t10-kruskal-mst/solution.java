    static int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    static long solve(long n, long m, long[][] e) {
        int nn = (int) n;
        int mm = (int) m;
        Arrays.sort(e, (a, b) -> Long.compare(a[2], b[2]));
        int[] parent = new int[nn + 1];
        int[] size = new int[nn + 1];
        for (int i = 0; i <= nn; ++i) {
            parent[i] = i;
            size[i] = 1;
        }
        long total = 0;
        long used = 0;
        for (int i = 0; i < mm; ++i) {
            int a = find(parent, (int) e[i][0]);
            int b = find(parent, (int) e[i][1]);
            if (a == b) continue;
            if (size[a] < size[b]) {
                int t = a;
                a = b;
                b = t;
            }
            parent[b] = a;
            size[a] += size[b];
            total += e[i][2];
            ++used;
            if (used == n - 1) break;
        }
        if (used != n - 1) return -1;
        return total;
    }
