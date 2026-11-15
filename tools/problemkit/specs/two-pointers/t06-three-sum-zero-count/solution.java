    static long solve(long n, long[] a) {
        long[] b = a.clone();
        Arrays.sort(b);
        int total = (int) n;
        long count = 0;
        for (int i = 0; i + 2 < total; ++i) {
            int lo = i + 1, hi = total - 1;
            while (lo < hi) {
                long sum = b[i] + b[lo] + b[hi];
                if (sum < 0) {
                    lo++;
                } else if (sum > 0) {
                    hi--;
                } else if (b[lo] == b[hi]) {
                    long m = hi - lo + 1;
                    count += m * (m - 1) / 2;
                    break;
                } else {
                    long lowCount = 1;
                    while (lo + lowCount < hi && b[lo + (int) lowCount] == b[lo]) lowCount++;
                    long highCount = 1;
                    while (hi - highCount > lo && b[hi - (int) highCount] == b[hi]) highCount++;
                    count += lowCount * highCount;
                    lo += (int) lowCount;
                    hi -= (int) highCount;
                }
            }
        }
        return count;
    }
