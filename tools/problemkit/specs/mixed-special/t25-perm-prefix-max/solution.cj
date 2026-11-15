package t25_perm_prefix_max

func solve(n: Int64, k: Int64): Array<Int64> {
    let p = Array<Int64>(n, repeat: 0)
    var at: Int64 = 0
    var x: Int64 = 1
    while (x <= k - 1) {
        p[at] = x
        at += 1
        x += 1
    }
    x = n
    while (x >= k) {
        p[at] = x
        at += 1
        x -= 1
    }
    return p
}
