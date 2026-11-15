package t17_stone_merge

func solve(n: Int64, a: Array<Int64>): Int64 {
    if (n <= 1) {
        return 0
    }
    let pre = Array<Int64>(n + 1, repeat: 0)
    for (i in 0..n) {
        pre[i + 1] = pre[i] + a[i]
    }
    let dp = Array<Array<Int64>>(n, { _ => Array<Int64>(n, repeat: 0) })
    for (len in 2..n + 1) {
        for (i in 0..n - len + 1) {
            let j = i + len - 1
            var best = -1
            for (k in i..j) {
                let cand = dp[i][k] + dp[k + 1][j]
                if (best < 0 || cand < best) {
                    best = cand
                }
            }
            dp[i][j] = best + pre[j + 1] - pre[i]
        }
    }
    return dp[0][n - 1]
}
