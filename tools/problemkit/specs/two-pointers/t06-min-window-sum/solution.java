    static long solve(long n, long s, long[] a) {
        long best = -1, sum = 0;
        int left = 0;
        for (int right = 0; right < (int) n; ++right) {
            sum += a[right];
            while (sum >= s) {
                long length = right - left + 1;
                if (best < 0 || length < best) best = length;
                sum -= a[left];
                left++;
            }
        }
        return best < 0 ? 0 : best;
    }
