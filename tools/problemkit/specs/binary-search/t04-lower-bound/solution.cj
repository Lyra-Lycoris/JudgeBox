package t04_lower_bound

func solve(n: Int64, a: Array<Int64>, x: Int64): Int64 {
    var lo = 0
    var hi = n
    while (lo < hi) {
        let mid = lo + (hi - lo) / 2
        if (a[mid] >= x) {
            hi = mid
        } else {
            lo = mid + 1
        }
    }
    return lo
}
