package t16_max_subarray

func solve(n: Int64, a: Array<Int64>): Int64 {
    var best = a[0]
    var cur = a[0]
    for (i in 1..n) {
        let x = a[i]
        if (cur > 0) {
            cur = cur + x
        } else {
            cur = x
        }
        if (cur > best) {
            best = cur
        }
    }
    return best
}
