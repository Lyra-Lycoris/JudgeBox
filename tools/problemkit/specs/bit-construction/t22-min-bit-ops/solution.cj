package t22_min_bit_ops

func solve(n: Int64): Int64 {
    var x = n
    var ops: Int64 = 0
    while (x > 0) {
        if (x % 2 == 0) {
            x = x / 2
        } else if (x == 3 || x % 4 == 1) {
            x = x - 1
        } else {
            x = x + 1
        }
        ops += 1
    }
    return ops
}
