package t23_hanoi_moves

func solve(n: Int64): Int64 {
    var power: Int64 = 1
    for (_ in 0..n) {
        power *= 2
    }
    return power - 1
}
