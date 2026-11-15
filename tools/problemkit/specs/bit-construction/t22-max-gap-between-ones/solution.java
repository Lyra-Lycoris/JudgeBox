    static long solve(long n) {
        long best = 0;
        long last = -1;
        long pos = 0;
        while (n > 0) {
            if ((n & 1L) != 0) {
                if (last >= 0) {
                    long gap = pos - last - 1;
                    if (gap > best) best = gap;
                }
                last = pos;
            }
            n >>= 1;
            ++pos;
        }
        return best;
    }
