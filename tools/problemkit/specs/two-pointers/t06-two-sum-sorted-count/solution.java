    static long solve(long n, long target, long[] a) {
        int i = 0, j = (int) n - 1;
        long count = 0;
        while (i < j) {
            long sum = a[i] + a[j];
            if (sum < target) {
                i++;
            } else if (sum > target) {
                j--;
            } else {
                if (a[i] == a[j]) {
                    long m = j - i + 1;
                    count += m * (m - 1) / 2;
                    break;
                }
                long leftCount = 1;
                while (i + leftCount < j && a[i + (int) leftCount] == a[i]) leftCount++;
                long rightCount = 1;
                while (j - rightCount > i && a[j - (int) rightCount] == a[j]) rightCount++;
                count += leftCount * rightCount;
                i += (int) leftCount;
                j -= (int) rightCount;
            }
        }
        return count;
    }
