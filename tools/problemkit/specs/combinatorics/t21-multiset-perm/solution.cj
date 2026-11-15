package t21_multiset_perm

import std.sort.*

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

func solve(n: Int64, a: Array<Int64>): Int64 {
    let MOD: Int64 = 1000000007
    let sorted = a.clone()
    sort(sorted)
    let fact = Array<Int64>(n + 1, repeat: 0)
    fact[0] = 1
    var i: Int64 = 1
    while (i <= n) {
        fact[i] = fact[i - 1] * (i % MOD) % MOD
        i += 1
    }
    let invfact = Array<Int64>(n + 1, repeat: 0)
    invfact[n] = powMod(fact[n], MOD - 2)
    var j = n
    while (j >= 1) {
        invfact[j - 1] = invfact[j] * (j % MOD) % MOD
        j -= 1
    }
    var answer: Int64 = fact[n]
    var k: Int64 = 0
    while (k < n) {
        var e = k
        while (e < n && sorted[e] == sorted[k]) {
            e += 1
        }
        answer = answer * invfact[e - k] % MOD
        k = e
    }
    return answer
}
