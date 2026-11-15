package t06_longest_ones_after_delete

func solve(n: Int64, a: Array<Int64>): Int64 {
    var best: Int64 = 0
    var zeros: Int64 = 0
    var left: Int64 = 0
    var right: Int64 = 0
    while (right < n) {
        if (a[right] == 0) {
            zeros += 1
        }
        while (zeros > 1) {
            if (a[left] == 0) {
                zeros -= 1
            }
            left += 1
        }
        if (right - left + 1 > best) {
            best = right - left + 1
        }
        right += 1
    }
    if (best > 0) {
        return best - 1
    }
    return 0
}
