    static int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    static boolean solve(long n, long m, long[][] e) {
        int nn = (int) n;
        int[] parent = new int[nn + 1];
        int[] size = new int[nn + 1];
        for (int i = 0; i <= nn; ++i) {
            parent[i] = i;
            size[i] = 1;
        }
        int mm = (int) m;
        for (int i = 0; i < mm; ++i) {
            int a = find(parent, (int) e[i][0]);
            int b = find(parent, (int) e[i][1]);
            if (a == b) return true;
            if (size[a] < size[b]) {
                int t = a;
                a = b;
                b = t;
            }
            parent[b] = a;
            size[a] += size[b];
        }
        return false;
    }
