    static long[] solve(long n, long[] a, long q, long[][] queries) {
        int size = (int) n;
        long[] values = new long[size];
        for (int i = 0; i < size; ++i) values[i] = a[i];
        Arrays.sort(values);
        int m = 0;
        for (int i = 0; i < size; ++i) {
            if (i == 0 || values[i] != values[i - 1]) values[m++] = values[i];
        }
        int[] last = new int[m + 1];

        int[] head = new int[size + 1];
        Arrays.fill(head, -1);
        int[] nxt = new int[(int) q];
        for (int j = 0; j < (int) q; ++j) {
            int r = (int) queries[j][1];
            nxt[j] = head[r];
            head[r] = j;
        }

        int[] tree = new int[size + 1];
        long[] answer = new long[(int) q];
        for (int r = 1; r <= size; ++r) {
            int id = Arrays.binarySearch(values, 0, m, a[r - 1]) + 1;
            if (last[id] != 0) {
                for (int i = last[id]; i <= size; i += i & -i) tree[i] -= 1;
            }
            last[id] = r;
            for (int i = r; i <= size; i += i & -i) tree[i] += 1;

            int upto = 0;
            for (int i = r; i > 0; i -= i & -i) upto += tree[i];

            for (int j = head[r]; j != -1; j = nxt[j]) {
                int s = 0;
                for (int i = (int) queries[j][0] - 1; i > 0; i -= i & -i) s += tree[i];
                answer[j] = upto - s;
            }
        }
        return answer;
    }
