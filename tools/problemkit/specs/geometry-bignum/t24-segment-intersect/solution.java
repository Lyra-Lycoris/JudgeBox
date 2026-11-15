    static long crossOf(long ax, long ay, long bx, long by, long cx, long cy) {
        return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax);
    }

    static boolean betweenValues(long lo1, long lo2, long value) {
        long low = Math.min(lo1, lo2);
        long high = Math.max(lo1, lo2);
        return low <= value && value <= high;
    }

    static boolean onSegment(long ax, long ay, long bx, long by, long px, long py) {
        return betweenValues(ax, bx, px) && betweenValues(ay, by, py);
    }

    static boolean solve(long ax, long ay, long bx, long by, long cx, long cy, long dx, long dy) {
        long d1 = crossOf(ax, ay, bx, by, cx, cy);
        long d2 = crossOf(ax, ay, bx, by, dx, dy);
        long d3 = crossOf(cx, cy, dx, dy, ax, ay);
        long d4 = crossOf(cx, cy, dx, dy, bx, by);
        if (((d1 > 0 && d2 < 0) || (d1 < 0 && d2 > 0)) && ((d3 > 0 && d4 < 0) || (d3 < 0 && d4 > 0))) {
            return true;
        }
        if (d1 == 0 && onSegment(ax, ay, bx, by, cx, cy)) return true;
        if (d2 == 0 && onSegment(ax, ay, bx, by, dx, dy)) return true;
        if (d3 == 0 && onSegment(cx, cy, dx, dy, ax, ay)) return true;
        if (d4 == 0 && onSegment(cx, cy, dx, dy, bx, by)) return true;
        return false;
    }
