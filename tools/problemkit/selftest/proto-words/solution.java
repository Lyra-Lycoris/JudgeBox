    static boolean solve(long k, String[] w) {
        for (int i = 1; i < w.length; ++i) if (!w[i].equals(w[0])) return false;
        return true;
    }
