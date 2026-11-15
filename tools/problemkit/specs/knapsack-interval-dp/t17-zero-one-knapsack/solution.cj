package t17_zero_one_knapsack

func solve(n: Int64, cap: Int64, w: Array<Int64>, v: Array<Int64>): Int64 {
    let dp = Array<Int64>(cap + 1, repeat: 0)
    for (i in 0..n) {
        let wi = w[i]
        let vi = v[i]
        if (wi > cap) {
            continue
        }
        var j = cap
        while (j >= wi) {
            let cand = dp[j - wi] + vi
            if (cand > dp[j]) {
                dp[j] = cand
            }
            j -= 1
        }
    }
    return dp[cap]
}
