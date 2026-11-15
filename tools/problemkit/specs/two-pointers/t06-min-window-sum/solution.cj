package t06_min_window_sum

func solve(n: Int64, s: Int64, a: Array<Int64>): Int64 {
    var best: Int64 = -1
    var sum: Int64 = 0
    var left: Int64 = 0
    var right: Int64 = 0
    while (right < n) {
        sum += a[right]
        while (sum >= s) {
            let length = right - left + 1
            if (best < 0 || length < best) {
                best = length
            }
            sum -= a[left]
            left += 1
        }
        right += 1
    }
    if (best < 0) {
        return 0
    }
    return best
}
