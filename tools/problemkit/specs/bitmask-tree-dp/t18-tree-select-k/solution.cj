package t18_tree_select_k

func solve(n: Int64, k: Int64, w: Array<Int64>, p: Array<Int64>): Int64 {
    let NEG: Int64 = 0 - (1 << 62)
    let K = k
    let dp = Array<Array<Int64>>(n + 1, { _ => Array<Int64>(K + 1, repeat: NEG) })
    let sz = Array<Int64>(n + 1, repeat: 1)
    var i: Int64 = 1
    while (i <= n) {
        dp[i][0] = 0
        dp[i][1] = w[i - 1]
        i += 1
    }
    i = n
    while (i >= 2) {
        let par = p[i - 2]
        var si = sz[i]
        if (si > K) {
            si = K
        }
        var sv = sz[par]
        if (sv > K) {
            sv = K
        }
        var lim = si + sv
        if (lim > K) {
            lim = K
        }
        var j = lim
        while (j >= 1) {
            var best = dp[par][j]
            var lo = j - sv
            if (lo < 1) {
                lo = 1
            }
            var hi = j - 1
            if (hi > si) {
                hi = si
            }
            var t = lo
            while (t <= hi) {
                let a = dp[par][j - t]
                let b = dp[i][t]
                if (a != NEG && b != NEG) {
                    let val = a + b
                    if (val > best) {
                        best = val
                    }
                }
                t += 1
            }
            dp[par][j] = best
            j -= 1
        }
        sz[par] += sz[i]
        i -= 1
    }
    return dp[1][K]
}
