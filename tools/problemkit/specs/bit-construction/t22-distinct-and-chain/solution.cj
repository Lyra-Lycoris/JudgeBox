package t22_distinct_and_chain

func solve(n: Int64): Array<Int64> {
    let shift: Int64 = 40
    let a = Array<Int64>(n, repeat: 0)
    var value: Int64 = 1
    for (i in 0..n) {
        if (i % 2 == 0) {
            a[i] = value
        } else {
            a[i] = value << shift
            value += 1
        }
    }
    return a
}
