package t23_fast_pow

func powMod(base: Int64, exp: Int64, mod: Int64): Int64 {
    if (exp == 0) {
        return 1 % mod
    }
    let half = powMod(base, exp / 2, mod)
    var result = half * half % mod
    if ((exp & 1) == 1) {
        result = result * (base % mod) % mod
    }
    return result
}

func solve(a: Int64, b: Int64, m: Int64): Int64 {
    return powMod(a % m, b, m)
}
