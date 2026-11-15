package t27_matrix_exp_recur

func solve(n: Int64, x: Int64, y: Int64, p: Int64, q: Int64): Int64 {
    let MOD: Int64 = 1000000007
    if (n == 0) {
        return x % MOD
    }
    if (n == 1) {
        return y % MOD
    }
    var m00 = p % MOD
    var m01 = q % MOD
    var m10: Int64 = 1
    var m11: Int64 = 0
    var r00: Int64 = 1
    var r01: Int64 = 0
    var r10: Int64 = 0
    var r11: Int64 = 1
    var e = n - 1
    while (e > 0) {
        if ((e & 1) == 1) {
            let t00 = (r00 * m00 + r01 * m10) % MOD
            let t01 = (r00 * m01 + r01 * m11) % MOD
            let t10 = (r10 * m00 + r11 * m10) % MOD
            let t11 = (r10 * m01 + r11 * m11) % MOD
            r00 = t00
            r01 = t01
            r10 = t10
            r11 = t11
        }
        let s00 = (m00 * m00 + m01 * m10) % MOD
        let s01 = (m00 * m01 + m01 * m11) % MOD
        let s10 = (m10 * m00 + m11 * m10) % MOD
        let s11 = (m10 * m01 + m11 * m11) % MOD
        m00 = s00
        m01 = s01
        m10 = s10
        m11 = s11
        e = e >> 1
    }
    return (r00 * y + r01 * x) % MOD
}
