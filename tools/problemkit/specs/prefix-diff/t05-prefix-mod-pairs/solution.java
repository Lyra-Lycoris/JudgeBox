    static long solve(long n, long[] a, long k) {
        int size = (int) n;
        long[] rems = new long[size + 1];
        long cur = 0;
        for (int i = 0; i < size; ++i) {
            cur = (cur + a[i]) % k;
            if (cur < 0) cur += k;
            rems[i + 1] = cur;
        }
        Arrays.sort(rems);
        long answer = 0;
        long run = 1;
        for (int i = 1; i <= size; ++i) {
            if (rems[i] == rems[i - 1]) {
                ++run;
            } else {
                answer += run * (run - 1) / 2;
                run = 1;
            }
        }
        answer += run * (run - 1) / 2;
        return answer;
    }
