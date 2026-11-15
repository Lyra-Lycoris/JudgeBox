package t22_and_zero_array

func solve(n: Int64): Array<Int64> {
    let a = Array<Int64>(n, repeat: 0)
    for (i in 0..n) {
        if (i % 2 == 0) {
            a[i] = 1
        } else {
            a[i] = 2
        }
    }
    return a
}
