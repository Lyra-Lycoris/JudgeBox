    static long solve(long n) {
        long x = n;
        long ops = 0;
        while (x > 0) {
            if (x % 2 == 0) {
                x /= 2;
            } else if (x == 3 || x % 4 == 1) {
                x -= 1;
            } else {
                x += 1;
            }
            ++ops;
        }
        return ops;
    }
