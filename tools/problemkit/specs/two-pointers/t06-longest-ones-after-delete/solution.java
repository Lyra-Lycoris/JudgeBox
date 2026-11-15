    static long solve(long n, long[] a) {
        long best = 0;
        int zeros = 0, left = 0;
        for (int right = 0; right < (int) n; ++right) {
            if (a[right] == 0) zeros++;
            while (zeros > 1) {
                if (a[left] == 0) zeros--;
                left++;
            }
            if (right - left + 1 > best) best = right - left + 1;
        }
        return best > 0 ? best - 1 : 0;
    }
