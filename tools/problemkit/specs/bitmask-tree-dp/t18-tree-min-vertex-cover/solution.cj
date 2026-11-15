package t18_tree_min_vertex_cover

func solve(n: Int64, p: Array<Int64>): Int64 {
    let dp0 = Array<Int64>(n + 1, repeat: 0)
    let dp1 = Array<Int64>(n + 1, repeat: 1)
    var i: Int64 = n
    while (i >= 2) {
        let par = p[i - 2]
        dp0[par] += dp1[i]
        if (dp0[i] < dp1[i]) {
            dp1[par] += dp0[i]
        } else {
            dp1[par] += dp1[i]
        }
        i -= 1
    }
    if (dp0[1] < dp1[1]) {
        return dp0[1]
    }
    return dp1[1]
}
