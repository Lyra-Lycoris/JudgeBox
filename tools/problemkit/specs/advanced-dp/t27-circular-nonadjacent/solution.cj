package t27_circular_nonadjacent

func __linear(a: Array<Int64>, lo: Int64, hi: Int64): Int64 {
    var p2: Int64 = 0
    var p1: Int64 = 0
    var i = lo
    while (i <= hi) {
        var cur = p2 + a[i]
        if (p1 > cur) {
            cur = p1
        }
        p2 = p1
        p1 = cur
        i += 1
    }
    return p1
}

func solve(n: Int64, a: Array<Int64>): Int64 {
    if (n == 1) {
        if (a[0] > 0) {
            return a[0]
        }
        return 0
    }
    let r1 = __linear(a, 0, n - 2)
    let r2 = __linear(a, 1, n - 1)
    if (r1 > r2) {
        return r1
    }
    return r2
}
