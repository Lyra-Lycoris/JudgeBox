    static final long NONE = Long.MAX_VALUE;

    static long[] treeSum;
    static long[] treeTag;

    static void build(long[] a, int node, int l, int r) {
        treeTag[node] = NONE;
        if (l == r) {
            treeSum[node] = a[l - 1];
            return;
        }
        int mid = (l + r) >>> 1;
        build(a, node << 1, l, mid);
        build(a, node << 1 | 1, mid + 1, r);
        treeSum[node] = treeSum[node << 1] + treeSum[node << 1 | 1];
    }

    static void applyNode(int node, int l, int r, long v) {
        treeSum[node] = v * (long) (r - l + 1);
        treeTag[node] = v;
    }

    static void push(int node, int l, int r) {
        if (treeTag[node] == NONE || l == r) return;
        int mid = (l + r) >>> 1;
        applyNode(node << 1, l, mid, treeTag[node]);
        applyNode(node << 1 | 1, mid + 1, r, treeTag[node]);
        treeTag[node] = NONE;
    }

    static void update(int node, int l, int r, int ql, int qr, long v) {
        if (ql <= l && r <= qr) {
            applyNode(node, l, r, v);
            return;
        }
        push(node, l, r);
        int mid = (l + r) >>> 1;
        if (ql <= mid) update(node << 1, l, mid, ql, qr, v);
        if (qr > mid) update(node << 1 | 1, mid + 1, r, ql, qr, v);
        treeSum[node] = treeSum[node << 1] + treeSum[node << 1 | 1];
    }

    static long[] solve(long n, long[] a, long q, long[][] ops) {
        int size = (int) n;
        treeSum = new long[4 * size + 4];
        treeTag = new long[4 * size + 4];
        build(a, 1, 1, size);
        long[] answer = new long[(int) q];
        for (int j = 0; j < (int) q; ++j) {
            update(1, 1, size, (int) ops[j][0], (int) ops[j][1], ops[j][2]);
            answer[j] = treeSum[1];
        }
        return answer;
    }
