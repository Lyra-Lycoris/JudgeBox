package t16_climb_stairs

func solve(n: Int64): Int64 {
    let MOD: Int64 = 1000000007
    var prev2: Int64 = 1
    var prev1: Int64 = 1
    if (n == 0) {
        return prev2
    }
    for (i in 2..=n) {
        let cur = (prev1 + prev2) % MOD
        prev2 = prev1
        prev1 = cur
    }
    return prev1
}
