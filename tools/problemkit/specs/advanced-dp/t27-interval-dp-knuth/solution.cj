package t27_interval_dp_knuth

func solve(n: Int64, a: Array<Int64>): Int64 {
    if (n <= 1) {
        return 0
    }
    let w = n + 1
    let size = w * w
    let dp = Array<Int64>(size, repeat: 0)
    let opt = Array<Int64>(size, repeat: 0)
    let pre = Array<Int64>(w, repeat: 0)
    var i: Int64 = 1
    while (i <= n) {
        pre[i] = pre[i - 1] + a[i - 1]
        i += 1
    }
    i = 1
    while (i <= n) {
        opt[i * w + i] = i
        i += 1
    }
    var length: Int64 = 2
    while (length <= n) {
        var l: Int64 = 1
        while (l + length - 1 <= n) {
            let r = l + length - 1
            let base = l * w
            let lo = opt[base + r - 1]
            var hi = opt[(l + 1) * w + r]
            if (hi > r - 1) {
                hi = r - 1
            }
            var best: Int64 = -1
            var bestk = lo
            var k = lo
            while (k <= hi) {
                let v = dp[base + k] + dp[(k + 1) * w + r]
                if (best < 0 || v < best) {
                    best = v
                    bestk = k
                }
                k += 1
            }
            dp[base + r] = best + pre[r] - pre[l - 1]
            opt[base + r] = bestk
            l += 1
        }
        length += 1
    }
    return dp[w + n]
}
