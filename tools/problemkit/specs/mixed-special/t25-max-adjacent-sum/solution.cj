package t25_max_adjacent_sum

func solve(n: Int64): Array<Int64> {
    let p = Array<Int64>(n, repeat: 0)
    var at: Int64 = 0
    p[at] = (n + 1) / 2
    at += 1
    var hi = n
    var lo: Int64 = 1
    while (at < n) {
        p[at] = hi
        at += 1
        hi -= 1
        if (at < n) {
            p[at] = lo
            at += 1
            lo += 1
        }
    }
    return p
}
