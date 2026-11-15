package t18_tree_max_independent_set

func solve(n: Int64, w: Array<Int64>, p: Array<Int64>): Int64 {
    let dp0 = Array<Int64>(n + 1, repeat: 0)
    let dp1 = Array<Int64>(n + 1, repeat: 0)
    var i: Int64 = 1
    while (i <= n) {
        dp1[i] = w[i - 1]
        i += 1
    }
    i = n
    while (i >= 2) {
        let par = p[i - 2]
        let a = dp0[i]
        let b = dp1[i]
        if (a > b) {
            dp0[par] += a
        } else {
            dp0[par] += b
        }
        dp1[par] += a
        i -= 1
    }
    if (dp0[1] > dp1[1]) {
        return dp0[1]
    }
    return dp1[1]
}
