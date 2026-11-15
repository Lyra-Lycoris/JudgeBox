package t28_max_min_segment_sum

func solve(n: Int64, k: Int64, a: Array<Int64>): Int64 {
    var total: Int64 = 0
    for (x in a) {
        total += x
    }
    var lo: Int64 = 0
    var hi: Int64 = total / k
    while (lo < hi) {
        let mid = (lo + hi + 1) / 2
        var cnt: Int64 = 0
        var cur: Int64 = 0
        for (x in a) {
            cur += x
            if (cur >= mid) {
                cnt += 1
                cur = 0
                if (cnt >= k) {
                    break
                }
            }
        }
        if (cnt >= k) {
            lo = mid
        } else {
            hi = mid - 1
        }
    }
    return lo
}
