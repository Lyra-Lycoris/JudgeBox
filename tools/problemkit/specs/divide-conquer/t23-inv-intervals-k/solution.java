    static void bitAdd(long[] tree, int size, int pos, long delta) {
        for (int i = pos; i <= size; i += i & -i) tree[i] += delta;
    }

    static long bitSum(long[] tree, int pos) {
        long sum = 0;
        for (int i = pos; i > 0; i -= i & -i) sum += tree[i];
        return sum;
    }

    static int lowerBound(long[] values, int len, long x) {
        int lo = 0, hi = len;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (values[mid] < x) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }

    static long solve(long n, long k, long[] a) {
        int len = (int) n;
        if (k <= 0) return n * (n + 1) / 2;
        long[] values = new long[len];
        System.arraycopy(a, 0, values, 0, len);
        Arrays.sort(values);
        int m = 0;
        for (int i = 0; i < len; ++i) {
            if (i == 0 || values[i] != values[i - 1]) values[m++] = values[i];
        }
        long[] tree = new long[m + 1];
        long answer = 0;
        long windowSize = 0;
        long inversions = 0;
        int right = 0;
        for (int left = 0; left < len; ++left) {
            while (right < len && inversions < k) {
                int pos = lowerBound(values, m, a[right]) + 1;
                inversions += windowSize - bitSum(tree, pos);
                bitAdd(tree, m, pos, 1);
                windowSize += 1;
                right += 1;
            }
            if (inversions >= k) answer += n - right + 1;
            int pos = lowerBound(values, m, a[left]) + 1;
            inversions -= bitSum(tree, pos - 1);
            bitAdd(tree, m, pos, -1);
            windowSize -= 1;
        }
        return answer;
    }
