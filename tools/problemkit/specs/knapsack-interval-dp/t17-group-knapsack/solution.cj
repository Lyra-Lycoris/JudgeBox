package t17_group_knapsack

import std.collection.*

func solve(n: Int64, cap: Int64, g: Array<Int64>, w: Array<Int64>, v: Array<Int64>): Int64 {
    let groups = Array<ArrayList<Int64>>(n + 2, { _ => ArrayList<Int64>() })
    for (i in 0..n) {
        groups[g[i]].add(i)
    }
    var dp = Array<Int64>(cap + 1, repeat: 0)
    for (key in 1..n + 1) {
        if (groups[key].size == 0) {
            continue
        }
        let ndp = dp.clone()
        for (idx in groups[key]) {
            if (w[idx] > cap) {
                continue
            }
            var j = cap
            while (j >= w[idx]) {
                let cand = dp[j - w[idx]] + v[idx]
                if (cand > ndp[j]) {
                    ndp[j] = cand
                }
                j -= 1
            }
        }
        dp = ndp
    }
    return dp[cap]
}
