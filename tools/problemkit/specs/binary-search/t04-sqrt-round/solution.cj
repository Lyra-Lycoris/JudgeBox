package t04_sqrt_round

func solve(x: Int64): Int64 {
    var lo = 0
    var hi = 1000000001
    while (lo + 1 < hi) {
        let mid = lo + (hi - lo) / 2
        let t = 2 * mid - 1
        if (t * t <= 4 * x * 1000000) {
            lo = mid
        } else {
            hi = mid
        }
    }
    return lo
}
