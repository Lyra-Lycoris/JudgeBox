package t17_bounded_knapsack

func solve(n: Int64, cap: Int64, w: Array<Int64>, v: Array<Int64>, c: Array<Int64>): Int64 {
    let dp = Array<Int64>(cap + 1, repeat: 0)
    for (i in 0..n) {
        let wi = w[i]
        let vi = v[i]
        var rest = c[i]
        var block = 1
        while (rest > 0) {
            var take = block
            if (rest < take) {
                take = rest
            }
            let bw = wi * take
            let bv = vi * take
            if (bw <= cap) {
                var j = cap
                while (j >= bw) {
                    let cand = dp[j - bw] + bv
                    if (cand > dp[j]) {
                        dp[j] = cand
                    }
                    j -= 1
                }
            }
            rest -= take
            block *= 2
        }
    }
    return dp[cap]
}
