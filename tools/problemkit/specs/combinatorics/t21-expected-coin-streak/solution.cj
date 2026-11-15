package t21_expected_coin_streak

func powMod(base: Int64, exp: Int64): Int64 {
    let MOD: Int64 = 1000000007
    var b = base % MOD
    var e = exp
    var result: Int64 = 1
    while (e > 0) {
        if (e % 2 == 1) {
            result = result * b % MOD
        }
        b = b * b % MOD
        e = e / 2
    }
    return result
}

func solve(n: Int64): Int64 {
    let MOD: Int64 = 1000000007
    var answer = powMod(2, n + 1) - 2
    if (answer < 0) {
        answer += MOD
    }
    return answer
}
