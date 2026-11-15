package t19_bracket_sequences

func powerMod(base: Int64, exponent: Int64, mod: Int64): Int64 {
    var result: Int64 = 1
    var b = base % mod
    var e = exponent
    while (e > 0) {
        if (e % 2 == 1) {
            result = result * b % mod
        }
        b = b * b % mod
        e = e / 2
    }
    return result
}

func solve(n: Int64): Int64 {
    let MOD: Int64 = 1000000007
    var factorialN: Int64 = 1
    var i: Int64 = 2
    while (i <= n) {
        factorialN = factorialN * i % MOD
        i += 1
    }
    var upper: Int64 = 1
    i = n + 1
    while (i <= 2 * n) {
        upper = upper * i % MOD
        i += 1
    }
    let binomial = upper * powerMod(factorialN, MOD - 2, MOD) % MOD
    return binomial * powerMod(n + 1, MOD - 2, MOD) % MOD
}
