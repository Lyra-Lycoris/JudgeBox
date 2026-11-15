package t21_derangement

func solve(n: Int64): Int64 {
    let MOD: Int64 = 1000000007
    if (n == 0) {
        return 1
    }
    if (n == 1) {
        return 0
    }
    var prev2: Int64 = 1
    var prev1: Int64 = 0
    for (i in 2..=n) {
        let cur = ((i - 1) % MOD) * ((prev1 + prev2) % MOD) % MOD
        prev2 = prev1
        prev1 = cur
    }
    return prev1
}
