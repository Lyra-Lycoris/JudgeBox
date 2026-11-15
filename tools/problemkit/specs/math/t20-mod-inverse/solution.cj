package t20_mod_inverse

func solve(a: Int64, m: Int64): Int64 {
    var oldR = a
    var r = m
    var oldS = 1
    var s = 0
    while (r != 0) {
        let q = oldR / r
        let nextR = oldR - q * r
        oldR = r
        r = nextR
        let nextS = oldS - q * s
        oldS = s
        s = nextS
    }
    if (oldR != 1) {
        return -1
    }
    var inv = oldS % m
    if (inv < 0) {
        inv += m
    }
    return inv
}
