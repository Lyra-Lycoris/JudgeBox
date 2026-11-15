package t24_segment_intersect

func crossOf(ax: Int64, ay: Int64, bx: Int64, by: Int64, cx: Int64, cy: Int64): Int64 {
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
}

func betweenValue(lo1: Int64, lo2: Int64, value: Int64): Bool {
    var low = lo1
    var high = lo2
    if (low > high) {
        low = lo2
        high = lo1
    }
    return low <= value && value <= high
}

func onSegment(ax: Int64, ay: Int64, bx: Int64, by: Int64, px: Int64, py: Int64): Bool {
    return betweenValue(ax, bx, px) && betweenValue(ay, by, py)
}

func solve(ax: Int64, ay: Int64, bx: Int64, by: Int64,
           cx: Int64, cy: Int64, dx: Int64, dy: Int64): Bool {
    let d1 = crossOf(ax, ay, bx, by, cx, cy)
    let d2 = crossOf(ax, ay, bx, by, dx, dy)
    let d3 = crossOf(cx, cy, dx, dy, ax, ay)
    let d4 = crossOf(cx, cy, dx, dy, bx, by)
    if (((d1 > 0 && d2 < 0) || (d1 < 0 && d2 > 0)) && ((d3 > 0 && d4 < 0) || (d3 < 0 && d4 > 0))) {
        return true
    }
    if (d1 == 0 && onSegment(ax, ay, bx, by, cx, cy)) {
        return true
    }
    if (d2 == 0 && onSegment(ax, ay, bx, by, dx, dy)) {
        return true
    }
    if (d3 == 0 && onSegment(cx, cy, dx, dy, ax, ay)) {
        return true
    }
    if (d4 == 0 && onSegment(cx, cy, dx, dy, bx, by)) {
        return true
    }
    return false
}
