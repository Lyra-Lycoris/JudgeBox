    static boolean solve(long n, long[] a, long target) {
        Set<Long> seen = new HashSet<>();
        for (long x : a) {
            if (seen.contains(target - x)) return true;
            seen.add(x);
        }
        return false;
    }
