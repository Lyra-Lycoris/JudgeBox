    static long solve(long n, long[] a) {
        int size = (int) n;
        long[] values = new long[size];
        for (int i = 0; i < size; ++i) values[i] = a[i];
        Arrays.sort(values);
        int m = 0;
        for (int i = 0; i < size; ++i) {
            if (i == 0 || values[i] != values[i - 1]) values[m++] = values[i];
        }
        long[] tree = new long[m + 1];
        long answer = 0;
        for (int k = 0; k < size; ++k) {
            int p = Arrays.binarySearch(values, 0, m, a[k]) + 1;
            long notGreater = 0;
            for (int i = p; i > 0; i -= i & -i) notGreater += tree[i];
            answer += k - notGreater;
            for (int i = p; i <= m; i += i & -i) tree[i] += 1;
        }
        return answer;
    }
