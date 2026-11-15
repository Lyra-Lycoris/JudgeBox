    static long countUpto(long n, long zeroMask, long oneMask) {
        if ((zeroMask & oneMask) != 0) return 0;
        long both = zeroMask | oneMask;
        long total = 0;
        boolean ok = true;
        for (int i = 59; i >= 0; --i) {
            long nb = (n >>> i) & 1L;
            long forcedOne = (oneMask >>> i) & 1L;
            if (forcedOne == 1L) {
                if (nb == 0L) {
                    ok = false;
                    break;
                }
            } else if (nb == 1L) {
                long lowMask = (1L << i) - 1L;
                int freeBits = i - Long.bitCount(both & lowMask);
                total += 1L << freeBits;
                if (((zeroMask >>> i) & 1L) == 1L) {
                    ok = false;
                    break;
                }
            }
        }
        if (ok) total += 1L;
        if (oneMask == 0L) total -= 1L;
        return total;
    }

    static long solve(long n, long m, long[][] cond) {
        int mm = (int) m;
        long[] groups = new long[mm + 1];
        int masks = 1 << mm;
        for (int mask = 1; mask < masks; ++mask) {
            long zeroMask = 0L, oneMask = 0L;
            int size = 0;
            for (int i = 0; i < mm; ++i) {
                if (((mask >>> i) & 1) == 0) continue;
                ++size;
                long t = cond[i][0], x = cond[i][1];
                if (t == 1L) {
                    zeroMask |= x - 1L;
                } else {
                    oneMask |= 1L << x;
                }
            }
            if ((zeroMask & oneMask) != 0L) continue;
            groups[size] += countUpto(n, zeroMask, oneMask);
        }
        long answer = 0L;
        for (int size = 1; size <= mm; ++size) {
            if ((size & 1) == 1) answer += groups[size];
            else answer -= groups[size];
        }
        return answer;
    }
