    static long countLE(long[] arr, long x) {
        int lo = 0, hi = arr.length;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (arr[mid] <= x) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }

    static long kthSmallest(long[] a, long[] b, long t) {
        long lo = -1000000001L, hi = 1000000001L;
        while (lo < hi) {
            long mid = lo + (hi - lo) / 2;
            if (countLE(a, mid) + countLE(b, mid) >= t) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }

    static long solve(long n, long[] a, long m, long[] b) {
        long total = n + m;
        return kthSmallest(a, b, (total + 1) / 2) + kthSmallest(a, b, (total + 2) / 2);
    }
