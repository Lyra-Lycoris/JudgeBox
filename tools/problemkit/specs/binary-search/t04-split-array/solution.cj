package t04_split_array

func solve(n: Int64, a: Array<Int64>, k: Int64): Int64 {
    var lo = 0
    var hi = 0
    for (x in a) {
        if (x > lo) {
            lo = x
        }
        hi += x
    }
    while (lo < hi) {
        let mid = lo + (hi - lo) / 2
        var parts = 1
        var cur = 0
        for (x in a) {
            if (cur + x > mid) {
                parts += 1
                cur = x
                if (parts > k) {
                    break
                }
            } else {
                cur += x
            }
        }
        if (parts <= k) {
            hi = mid
        } else {
            lo = mid + 1
        }
    }
    return lo
}
