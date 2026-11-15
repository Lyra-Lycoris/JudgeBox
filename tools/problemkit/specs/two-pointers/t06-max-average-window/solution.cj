package t06_max_average_window

func absOf(x: Int64): Int64 {
    if (x < 0) {
        return -x
    }
    return x
}

func gcdOf(a: Int64, b: Int64): Int64 {
    var x = absOf(a)
    var y = absOf(b)
    while (y != 0) {
        let t = x % y
        x = y
        y = t
    }
    return x
}

func solve(n: Int64, k: Int64, a: Array<Int64>): String {
    var sum: Int64 = 0
    for (i in 0..k) {
        sum += a[i]
    }
    var best = sum
    var i = k
    while (i < n) {
        sum += a[i] - a[i - k]
        if (sum > best) {
            best = sum
        }
        i += 1
    }
    let g = gcdOf(best, k)
    var p = best / g
    var q = k / g
    if (q < 0) {
        p = -p
        q = -q
    }
    return p.toString() + "/" + q.toString()
}
