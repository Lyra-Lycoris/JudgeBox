package t18_hamilton_path

func solve(n: Int64, w: Array<Array<Int64>>): Int64 {
    let INF: Int64 = 1 << 62
    if (n == 1) {
        return 0
    }
    let size: Int64 = 1 << n
    let full: Int64 = size - 1
    let dp = Array<Array<Int64>>(size, { _ => Array<Int64>(n, repeat: INF) })
    dp[1][0] = 0
    var mask: Int64 = 1
    while (mask < size) {
        let rest = full ^ mask
        var v: Int64 = 0
        while (v < n) {
            let cur = dp[mask][v]
            if (cur < INF) {
                var u: Int64 = 0
                while (u < n) {
                    let bit: Int64 = 1 << u
                    if ((rest & bit) != 0) {
                        let val = cur + w[v][u]
                        if (val < dp[mask | bit][u]) {
                            dp[mask | bit][u] = val
                        }
                    }
                    u += 1
                }
            }
            v += 1
        }
        mask += 2
    }
    return dp[full][n - 1]
}
