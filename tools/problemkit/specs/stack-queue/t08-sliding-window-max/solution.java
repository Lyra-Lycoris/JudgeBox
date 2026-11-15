    static long[] solve(long n, long k, long[] a) {
        int size = (int) n;
        int[] window = new int[size + 1];
        int head = 0;
        int tail = 0;
        long[] answer = new long[size - (int) k + 1];
        int count = 0;
        for (int i = 0; i < size; ++i) {
            while (tail > head && a[window[tail - 1]] <= a[i]) tail -= 1;
            window[tail++] = i;
            if (window[head] <= i - k) head += 1;
            if (i >= k - 1) answer[count++] = a[window[head]];
        }
        return answer;
    }
