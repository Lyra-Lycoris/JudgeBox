package t20_divisor_count

func solve(n: Int64): Int64 {
    var count = 0
    var d = 1
    while (d * d <= n) {
        if (n % d == 0) {
            if (d * d == n) {
                count += 1
            } else {
                count += 2
            }
        }
        d += 1
    }
    return count
}
