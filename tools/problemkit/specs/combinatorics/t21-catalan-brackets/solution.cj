package t21_catalan_brackets

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
    var numerator: Int64 = 1
    var denominator: Int64 = 1
    for (i in 1..=n) {
        numerator = numerator * ((n + i) % MOD) % MOD
        denominator = denominator * (i % MOD) % MOD
    }
    denominator = denominator * ((n + 1) % MOD) % MOD
    return numerator * powMod(denominator, MOD - 2) % MOD
}
