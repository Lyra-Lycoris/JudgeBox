    static long[] solve(long n, long r, long[] ch) {
        int N = (int) n;
        long[] answer = new long[N];
        int written = 0;
        int[] cur = new int[N];
        int[] nxt = new int[N];
        int curSize = 1;
        cur[0] = (int) r;
        boolean forward = true;
        while (curSize > 0) {
            if (forward) {
                for (int i = 0; i < curSize; ++i) answer[written++] = cur[i];
            } else {
                for (int i = curSize - 1; i >= 0; --i) answer[written++] = cur[i];
            }
            int nextSize = 0;
            for (int i = 0; i < curSize; ++i) {
                int v = cur[i];
                int left = (int) ch[2 * (v - 1)];
                int right = (int) ch[2 * (v - 1) + 1];
                if (left != 0) nxt[nextSize++] = left;
                if (right != 0) nxt[nextSize++] = right;
            }
            int[] tmp = cur;
            cur = nxt;
            nxt = tmp;
            curSize = nextSize;
            forward = !forward;
        }
        return answer;
    }
