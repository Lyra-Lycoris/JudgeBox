    static long solve(long n, long[] h) {
        int left = 0;
        int right = (int) n - 1;
        long leftMax = 0;
        long rightMax = 0;
        long water = 0;
        while (left <= right) {
            if (h[left] <= h[right]) {
                if (h[left] >= leftMax) leftMax = h[left];
                else water += leftMax - h[left];
                left += 1;
            } else {
                if (h[right] >= rightMax) rightMax = h[right];
                else water += rightMax - h[right];
                right -= 1;
            }
        }
        return water;
    }
