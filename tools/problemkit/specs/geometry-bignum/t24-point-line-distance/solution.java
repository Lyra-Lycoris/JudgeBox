    static boolean solve(long x1, long y1, long x2, long y2, long px, long py, long d) {
        long dx = x2 - x1;
        long dy = y2 - y1;
        long cross = dx * (py - y1) - dy * (px - x1);
        long len2 = dx * dx + dy * dy;
        return cross * cross <= d * d * len2;
    }
