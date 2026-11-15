    static long solve(long n, long[] a) {
        Map<Long, Long> diffCounts = new HashMap<>();
        Map<Long, Long> sumCounts = new HashMap<>();
        long answer = 0;
        for (int i = 0; i < n; ++i) {
            long index = i + 1L;
            long diffKey = a[i] - index;
            Long diffSeen = diffCounts.get(diffKey);
            if (diffSeen != null) answer += diffSeen;
            diffCounts.merge(diffKey, 1L, Long::sum);
            long sumKey = a[i] + index;
            Long sumSeen = sumCounts.get(sumKey);
            if (sumSeen != null) answer += sumSeen;
            sumCounts.merge(sumKey, 1L, Long::sum);
        }
        return answer;
    }
