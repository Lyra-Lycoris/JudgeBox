    static long solve(long a, long m) {
        long oldR = a, r = m;
        long oldS = 1, s = 0;
        while (r != 0) {
            long q = oldR / r;
            long nextR = oldR - q * r;
            oldR = r;
            r = nextR;
            long nextS = oldS - q * s;
            oldS = s;
            s = nextS;
        }
        if (oldR != 1) return -1;
        long inv = oldS % m;
        if (inv < 0) inv += m;
        return inv;
    }
