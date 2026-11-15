    static long solve(long n, long m) {
        long[] primes = new long[64];
        int k = 0;
        long x = m;
        if (x % 2 == 0) {
            primes[k++] = 2;
            while (x % 2 == 0) x /= 2;
        }
        for (long d = 3; d * d <= x; d += 2) {
            if (x % d == 0) {
                primes[k++] = d;
                while (x % d == 0) x /= d;
            }
        }
        if (x > 1) primes[k++] = x;

        long answer = 0;
        for (long mask = 0; mask < (1L << k); ++mask) {
            long product = 1;
            long bits = 0;
            for (int j = 0; j < k; ++j) {
                if (((mask >> j) & 1L) == 1L) {
                    product *= primes[j];
                    bits++;
                }
            }
            long term = n / product;
            if (bits % 2 == 0) {
                answer += term;
            } else {
                answer -= term;
            }
        }
        return answer;
    }
