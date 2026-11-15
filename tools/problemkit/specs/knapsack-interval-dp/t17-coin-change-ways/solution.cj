package t17_coin_change_ways

func solve(n: Int64, target: Int64, coins: Array<Int64>): Int64 {
    let MOD = 1000000007
    let dp = Array<Int64>(target + 1, repeat: 0)
    dp[0] = 1
    for (i in 0..n) {
        let c = coins[i]
        if (c > target) {
            continue
        }
        var j = c
        while (j <= target) {
            dp[j] = (dp[j] + dp[j - c]) % MOD
            j += 1
        }
    }
    return dp[target] % MOD
}
