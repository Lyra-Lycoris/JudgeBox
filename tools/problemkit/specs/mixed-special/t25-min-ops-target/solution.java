    static long solve(long n, long[] a, long[] b) {
        long answer = 0, prevPos = 0, prevNeg = 0;
        for (int i = 0; i < n; ++i) {
            long d = b[i] - a[i];
            long pos = d > 0 ? d : 0;
            long neg = d < 0 ? -d : 0;
            if (pos > prevPos) answer += pos - prevPos;
            if (neg > prevNeg) answer += neg - prevNeg;
            prevPos = pos;
            prevNeg = neg;
        }
        return answer;
    }
