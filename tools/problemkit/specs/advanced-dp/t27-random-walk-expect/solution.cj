package t27_random_walk_expect

func __modPow(base: Int64, exp: Int64, mod: Int64): Int64 {
    var result: Int64 = 1
    var b = base % mod
    var e = exp
    while (e > 0) {
        if ((e & 1) == 1) {
            result = result * b % mod
        }
        b = b * b % mod
        e = e >> 1
    }
    return result
}

func solve(n: Int64, p: Int64, q: Int64): Int64 {
    let MOD: Int64 = 1000000007
    let inv = __modPow((p + q) % MOD, MOD - 2, MOD)
    let pa = (p % MOD) * inv % MOD
    let pb = (q % MOD) * inv % MOD
    var e1: Int64 = 0
    var e2: Int64 = 0
    var cur: Int64 = 0
    var i: Int64 = 0
    while (i < n) {
        cur = (1 + pa * e1 + pb * e2) % MOD
        e2 = e1
        e1 = cur
        i += 1
    }
    return cur
}
