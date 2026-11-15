package t20_comb_mod

func modPow(base: Int64, exp: Int64, mod: Int64): Int64 {
    var b = base % mod
    var e = exp
    var result = 1 % mod
    while (e > 0) {
        if (e % 2 == 1) {
            result = result * b % mod
        }
        b = b * b % mod
        e = e / 2
    }
    return result
}

func solve(n: Int64, k: Int64, p: Int64): Int64 {
    if (k < 0 || k > n) {
        return 0
    }
    var r = k
    if (r > n - r) {
        r = n - r
    }
    var numerator = 1 % p
    var denominator = 1 % p
    var i = 1
    while (i <= r) {
        numerator = numerator * ((n - r + i) % p) % p
        denominator = denominator * (i % p) % p
        i += 1
    }
    return numerator * modPow(denominator, p - 2, p) % p
}
