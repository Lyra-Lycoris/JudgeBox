package t20_euler_phi

func solve(n: Int64): Int64 {
    var result = n
    var x = n
    var p = 2
    while (p * p <= x) {
        if (x % p == 0) {
            while (x % p == 0) {
                x = x / p
            }
            result -= result / p
        }
        p += 1
    }
    if (x > 1) {
        result -= result / x
    }
    return result
}
