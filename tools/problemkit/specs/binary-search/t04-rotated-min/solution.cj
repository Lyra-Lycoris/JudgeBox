package t04_rotated_min

func solve(n: Int64, a: Array<Int64>): Int64 {
    var lo = 0
    var hi = n - 1
    while (lo < hi) {
        let mid = lo + (hi - lo) / 2
        if (a[mid] > a[hi]) {
            lo = mid + 1
        } else {
            hi = mid
        }
    }
    return a[lo]
}
