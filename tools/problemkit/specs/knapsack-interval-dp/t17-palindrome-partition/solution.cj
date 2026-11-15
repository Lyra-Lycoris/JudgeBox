package t17_palindrome_partition

func solve(s: String): Int64 {
    let chars = s.toRuneArray()
    let n = chars.size
    if (n <= 1) {
        return 0
    }
    let dp = Array<Int64>(n + 1, repeat: n + 1)
    dp[0] = 0
    for (center in 0..n) {
        var l = center
        var r = center
        while (l >= 0 && r < n && chars[l] == chars[r]) {
            if (dp[l] + 1 < dp[r + 1]) {
                dp[r + 1] = dp[l] + 1
            }
            l -= 1
            r += 1
        }
        l = center
        r = center + 1
        while (l >= 0 && r < n && chars[l] == chars[r]) {
            if (dp[l] + 1 < dp[r + 1]) {
                dp[r + 1] = dp[l] + 1
            }
            l -= 1
            r += 1
        }
    }
    return dp[n] - 1
}
