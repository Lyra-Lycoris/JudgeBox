package t14_prim_manhattan_mst

func absVal(x: Int64): Int64 {
    if (x < 0) {
        return -x
    }
    return x
}

func solve(n: Int64, p: Array<Array<Int64>>): Int64 {
    let INF: Int64 = 1 << 62
    let best = Array<Int64>(n, repeat: INF)
    let used = Array<Bool>(n, repeat: false)
    best[0] = 0
    var total: Int64 = 0
    var round: Int64 = 0
    while (round < n) {
        var u: Int64 = -1
        var bd: Int64 = INF
        var i: Int64 = 0
        while (i < n) {
            if (!used[i] && best[i] < bd) {
                bd = best[i]
                u = i
            }
            i += 1
        }
        used[u] = true
        total += bd
        let xu = p[u][0]
        let yu = p[u][1]
        i = 0
        while (i < n) {
            if (!used[i]) {
                let d = absVal(p[i][0] - xu) + absVal(p[i][1] - yu)
                if (d < best[i]) {
                    best[i] = d
                }
            }
            i += 1
        }
        round += 1
    }
    return total
}
