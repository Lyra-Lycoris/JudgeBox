    static int kthLowerBound(long[] arr, int len, long x) {
        int lo = 0, hi = len;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (arr[mid] < x) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }

    static long[] solve(long n, long[] a, long m, long[][] queries) {
        int sz = (int) n;
        long[] values = Arrays.copyOf(a, sz);
        Arrays.sort(values);
        int uniq = 0;
        for (int i = 0; i < sz; ++i) {
            if (i == 0 || values[i] != values[i - 1]) values[uniq++] = values[i];
        }

        int depth = 1;
        while ((1L << depth) < uniq) depth++;
        int maxNodes = sz * (depth + 1) + 2;

        int[] leftChild = new int[maxNodes];
        int[] rightChild = new int[maxNodes];
        int[] total = new int[maxNodes];
        int[] root = new int[sz + 1];
        int nodes = 0;

        for (int i = 0; i < sz; ++i) {
            int pos = kthLowerBound(values, uniq, a[i]);
            int prev = root[i];
            nodes++;
            int node = nodes;
            total[node] = total[prev] + 1;
            leftChild[node] = leftChild[prev];
            rightChild[node] = rightChild[prev];
            root[i + 1] = node;

            int lo = 0, hi = uniq - 1;
            int curNew = node, curOld = prev;
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                nodes++;
                int child = nodes;
                if (pos <= mid) {
                    int oldChild = leftChild[curOld];
                    total[child] = total[oldChild] + 1;
                    leftChild[child] = leftChild[oldChild];
                    rightChild[child] = rightChild[oldChild];
                    leftChild[curNew] = child;
                    curNew = child;
                    curOld = oldChild;
                    hi = mid;
                } else {
                    int oldChild = rightChild[curOld];
                    total[child] = total[oldChild] + 1;
                    leftChild[child] = leftChild[oldChild];
                    rightChild[child] = rightChild[oldChild];
                    rightChild[curNew] = child;
                    curNew = child;
                    curOld = oldChild;
                    lo = mid + 1;
                }
            }
        }

        long[] answer = new long[(int) m];
        for (int t = 0; t < (int) m; ++t) {
            int l = (int) queries[t][0];
            int r = (int) queries[t][1];
            long k = queries[t][2];
            int rootR = root[r];
            int rootL = root[l - 1];
            int lo = 0, hi = uniq - 1;
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                int leftCount = total[leftChild[rootR]] - total[leftChild[rootL]];
                if (k <= leftCount) {
                    rootR = leftChild[rootR];
                    rootL = leftChild[rootL];
                    hi = mid;
                } else {
                    k -= leftCount;
                    rootR = rightChild[rootR];
                    rootL = rightChild[rootL];
                    lo = mid + 1;
                }
            }
            answer[t] = values[lo];
        }
        return answer;
    }
