package t19_distinct_subsequences

func solve(n: Int64, s: String): Int64 {
    let MOD: Int64 = 1000000007
    let chars = s.toRuneArray()
    var length = chars.size
    if (n < length) {
        length = n
    }
    if (length <= 0) {
        return 0
    }
    let dp = Array<Int64>(length + 1, repeat: 0)
    let last = Array<Int64>(26, repeat: -1)
    dp[0] = 1
    var i: Int64 = 1
    while (i <= length) {
        let c = Int64(UInt32(chars[i - 1])) - 97
        var value = 2 * dp[i - 1] % MOD
        if (last[c] >= 0) {
            value = (value - dp[last[c]] + MOD) % MOD
        }
        dp[i] = value
        last[c] = i - 1
        i += 1
    }
    return (dp[length] - 1 + MOD) % MOD
}
