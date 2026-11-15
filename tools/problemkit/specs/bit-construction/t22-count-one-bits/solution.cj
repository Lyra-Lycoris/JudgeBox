package t22_count_one_bits

func solve(n: Int64): Int64 {
    var x = n
    var count = 0
    while (x > 0) {
        x = x & (x - 1)
        count += 1
    }
    return count
}
