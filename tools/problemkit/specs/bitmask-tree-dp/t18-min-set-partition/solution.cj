package t18_min_set_partition

func solve(n: Int64, c: Array<Int64>): Int64 {
    let INF: Int64 = 1 << 62
    let size: Int64 = 1 << n
    let dp = Array<Int64>(size, repeat: INF)
    dp[0] = 0
    var mask: Int64 = 1
    while (mask < size) {
        var u: Int64 = 0
        while (((mask >> u) & 1) == 0) {
            u += 1
        }
        let low: Int64 = 1 << u
        let rest = mask ^ low
        var sub = rest
        var best = INF
        while (true) {
            let s = sub | low
            let v = dp[mask ^ s] + c[s]
            if (v < best) {
                best = v
            }
            if (sub == 0) {
                break
            }
            sub = (sub - 1) & rest
        }
        dp[mask] = best
        mask += 1
    }
    return dp[size - 1]
}
