package t23_dc_max_subarray

func solve(n: Int64, a: Array<Int64>): Int64 {
    var best = a[0]
    var current = a[0]
    for (i in 1..n) {
        let x = a[i]
        if (current > 0) {
            current = current + x
        } else {
            current = x
        }
        if (current > best) {
            best = current
        }
    }
    return best
}
