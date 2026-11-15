package t27_monotone_queue_jump

func solve(n: Int64, k: Int64, a: Array<Int64>): Int64 {
    let dp = Array<Int64>(n, repeat: 0)
    let q = Array<Int64>(n + 1, repeat: 0)
    dp[0] = a[0]
    var head: Int64 = 0
    var tail: Int64 = 1
    var i: Int64 = 1
    while (i < n) {
        let left = i - k
        while (head < tail && q[head] < left) {
            head += 1
        }
        dp[i] = a[i] + dp[q[head]]
        while (head < tail && dp[q[tail - 1]] >= dp[i]) {
            tail -= 1
        }
        q[tail] = i
        tail += 1
        i += 1
    }
    return dp[n - 1]
}
