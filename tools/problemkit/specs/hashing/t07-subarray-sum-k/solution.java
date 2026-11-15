    static long solve(long n, long k, long[] a) {
        Map<Long, Long> counts = new HashMap<>();
        counts.put(0L, 1L);
        long prefix = 0;
        long answer = 0;
        for (long x : a) {
            prefix += x;
            Long hit = counts.get(prefix - k);
            if (hit != null) answer += hit;
            counts.merge(prefix, 1L, Long::sum);
        }
        return answer;
    }
