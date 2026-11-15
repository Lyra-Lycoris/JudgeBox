package t04_find_peak

func solve(n: Int64, a: Array<Int64>): Int64 {
    var lo = 0
    var hi = n - 1
    while (lo < hi) {
        let mid = lo + (hi - lo) / 2
        if (a[mid] < a[mid + 1]) {
            lo = mid + 1
        } else {
            hi = mid
        }
    }
    return lo
}
