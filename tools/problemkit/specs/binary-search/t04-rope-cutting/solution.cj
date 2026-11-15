package t04_rope_cutting

func solve(n: Int64, a: Array<Int64>, k: Int64): Int64 {
    var lo = 0
    var hi = 0
    for (x in a) {
        if (x > hi) {
            hi = x
        }
    }
    while (lo < hi) {
        let mid = lo + (hi - lo + 1) / 2
        var cnt = 0
        for (x in a) {
            cnt += x / mid
            if (cnt >= k) {
                break
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
