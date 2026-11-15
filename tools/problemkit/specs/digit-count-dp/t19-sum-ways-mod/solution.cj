package t19_sum_ways_mod

func solve(n: Int64, m: Int64): Int64 {
    let MOD: Int64 = 1000000007
    if (n <= 0) {
        return 1
    }
    var limit = m
    if (limit > n) {
        limit = n
    }
    let dp = Array<Int64>(n + 1, repeat: 0)
    dp[0] = 1
    var window: Int64 = 1
    var i: Int64 = 1
    while (i <= n) {
        dp[i] = window % MOD
        var sub: Int64 = 0
        if (i >= limit) {
            sub = dp[i - limit]
        }
        window = (window + dp[i] - sub) % MOD
        if (window < 0) {
            window += MOD
        }
        i += 1
    }
    return dp[n]
}
