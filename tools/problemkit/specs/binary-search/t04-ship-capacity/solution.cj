package t04_ship_capacity

func solve(n: Int64, w: Array<Int64>, d: Int64): Int64 {
    var lo = 0
    var hi = 0
    for (x in w) {
        if (x > lo) {
            lo = x
        }
        hi += x
    }
    while (lo < hi) {
        let mid = lo + (hi - lo) / 2
        var days = 1
        var cur = 0
        for (x in w) {
            if (cur + x > mid) {
                days += 1
                cur = x
                if (days > d) {
                    break
                }
            } else {
                cur += x
            }
        }
        if (days <= d) {
            hi = mid
        } else {
            lo = mid + 1
        }
    }
    return lo
}
