package t05_max_average_k

func solve(n: Int64, k: Int64, a: Array<Int64>): Int64 {
    let pre = Array<Int64>(n + 1, repeat: 0)
    for (i in 0..n) {
        pre[i + 1] = pre[i] + a[i]
    }
    var lo: Int64 = -1000000000001
    var hi: Int64 = 1000000000000
    while (lo + 1 < hi) {
        let mid = lo + (hi - lo) / 2
        var best: Int64 = 0
        var feasible = false
        var j = k
        while (j <= n) {
            let i = j - k
            let candidate = pre[i] * 1000 - mid * i
            if (candidate < best) {
                best = candidate
            }
            if (pre[j] * 1000 - mid * j >= best) {
                feasible = true
                break
            }
            j = j + 1
        }
        if (feasible) {
            lo = mid
        } else {
            hi = mid
        }
    }
    return lo
}
