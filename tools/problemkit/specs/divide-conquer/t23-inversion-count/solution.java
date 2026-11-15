    static long mergeCount(long[] a, long[] tmp, int l, int r) {
        if (r - l <= 1) return 0;
        int mid = (l + r) >>> 1;
        long total = mergeCount(a, tmp, l, mid) + mergeCount(a, tmp, mid, r);
        int i = l, j = mid, k = l;
        while (i < mid && j < r) {
            if (a[i] <= a[j]) {
                tmp[k++] = a[i++];
            } else {
                tmp[k++] = a[j++];
                total += mid - i;
            }
        }
        while (i < mid) tmp[k++] = a[i++];
        while (j < r) tmp[k++] = a[j++];
        for (int p = l; p < r; ++p) a[p] = tmp[p];
        return total;
    }

    static long solve(long n, long[] a) {
        int len = (int) n;
        long[] work = new long[len];
        System.arraycopy(a, 0, work, 0, len);
        long[] tmp = new long[len];
        return mergeCount(work, tmp, 0, len);
    }
