    static long encodedCost(long length) {
        if (length <= 1) return 1;
        long value = length;
        long digits = 0;
        while (value > 0) {
            ++digits;
            value /= 10;
        }
        return 1 + digits;
    }

    static int upperBound(long[] values, int size, long target) {
        int lo = 0, hi = size;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (values[mid] <= target) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }

    static long[] solve(long n, String s, long q, long[][] qs) {
        int m = s.length();
        long[] runEnd = new long[m + 1];
        long[] prefix = new long[m + 2];
        int runs = 0;
        int index = 0;
        while (index < m) {
            int j = index + 1;
            while (j < m && s.charAt(j) == s.charAt(index)) ++j;
            runEnd[runs] = j;
            ++runs;
            prefix[runs] = prefix[runs - 1] + encodedCost(j - index);
            index = j;
        }
        long[] answer = new long[(int) q];
        for (int k = 0; k < q; ++k) {
            long left = qs[k][0];
            long right = qs[k][1];
            int low = upperBound(runEnd, runs, left - 1);
            int high = upperBound(runEnd, runs, right - 1);
            if (low == high) {
                answer[k] = encodedCost(right - left + 1);
            } else {
                long total = encodedCost(runEnd[low] - (left - 1));
                total += encodedCost(right - runEnd[high - 1]);
                total += prefix[high] - prefix[low + 1];
                answer[k] = total;
            }
        }
        return answer;
    }
