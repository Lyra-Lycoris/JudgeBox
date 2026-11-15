    static long[] solve(long n, long[] a) {
        int limit = 0;
        for (long x : a) if (x > limit) limit = (int) x;
        boolean[] sieve = new boolean[limit + 1];
        if (limit >= 0) sieve[0] = false;
        for (int i = 1; i <= limit; ++i) sieve[i] = true;
        if (limit >= 1) sieve[1] = false;
        for (int i = 2; (long) i * i <= limit; ++i) {
            if (sieve[i]) {
                for (long j = (long) i * i; j <= limit; j += i) sieve[(int) j] = false;
            }
        }
        int count = 0;
        for (int i = 0; i <= limit; ++i) if (sieve[i]) ++count;
        int[] primes = new int[count];
        int cursor = 0;
        for (int i = 0; i <= limit; ++i) if (sieve[i]) primes[cursor++] = i;
        long[] answer = new long[(int) n];
        for (int k = 0; k < n; ++k) {
            int lo = 0, hi = count;
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (primes[mid] <= a[k]) lo = mid + 1;
                else hi = mid;
            }
            answer[k] = lo;
        }
        return answer;
    }
