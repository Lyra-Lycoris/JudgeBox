    static int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    static long solve(long n, long m, long[][] g) {
        int nn = (int) n;
        int mm = (int) m;
        int total = nn * mm;
        int[] parent = new int[total];
        int[] size = new int[total];
        for (int i = 0; i < total; ++i) {
            parent[i] = i;
            size[i] = 1;
        }
        long islands = 0;
        for (int r = 0; r < nn; ++r) {
            for (int c = 0; c < mm; ++c) {
                if (g[r][c] != 1) continue;
                ++islands;
                int cur = r * mm + c;
                if (r > 0 && g[r - 1][c] == 1) {
                    int a = find(parent, cur);
                    int b = find(parent, cur - mm);
                    if (a != b) {
                        if (size[a] < size[b]) {
                            int t = a;
                            a = b;
                            b = t;
                        }
                        parent[b] = a;
                        size[a] += size[b];
                        --islands;
                    }
                }
                if (c > 0 && g[r][c - 1] == 1) {
                    int a = find(parent, cur);
                    int b = find(parent, cur - 1);
                    if (a != b) {
                        if (size[a] < size[b]) {
                            int t = a;
                            a = b;
                            b = t;
                        }
                        parent[b] = a;
                        size[a] += size[b];
                        --islands;
                    }
                }
            }
        }
        return islands;
    }
