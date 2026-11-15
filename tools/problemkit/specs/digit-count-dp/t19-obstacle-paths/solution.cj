package t19_obstacle_paths

func solve(n: Int64, m: Int64, g: Array<Array<Int64>>): Int64 {
    let MOD: Int64 = 1000000007
    let dp = Array<Int64>(m, repeat: 0)
    var i: Int64 = 0
    while (i < n) {
        var j: Int64 = 0
        while (j < m) {
            if (g[i][j] == 1) {
                dp[j] = 0
            } else if (i == 0 && j == 0) {
                dp[j] = 1
            } else {
                var left: Int64 = 0
                if (j > 0) {
                    left = dp[j - 1]
                }
                dp[j] = (dp[j] + left) % MOD
            }
            j += 1
        }
        i += 1
    }
    return dp[m - 1]
}
