package t14_bellman_ford_negative_cycle

func solve(n: Int64, m: Int64, s: Int64, e: Array<Array<Int64>>): Bool {
    let INF: Int64 = 1 << 62
    let dist = Array<Int64>(n + 1, repeat: INF)
    dist[s] = 0
    var round: Int64 = 0
    while (round < n) {
        var changed = false
        var i: Int64 = 0
        while (i < m) {
            let u = e[i][0]
            let v = e[i][1]
            let w = e[i][2]
            if (dist[u] < INF) {
                let nd = dist[u] + w
                if (nd < dist[v]) {
                    dist[v] = nd
                    changed = true
                }
            }
            i += 1
        }
        if (!changed) {
            return false
        }
        round += 1
    }
    return true
}
