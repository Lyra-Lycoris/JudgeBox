package t20_fast_pow

func solve(a: Int64, b: Int64, m: Int64): Int64 {
    if (m == 1) {
        return 0
    }
    var base = a % m
    var exp = b
    var result = 1 % m
    while (exp > 0) {
        if (exp % 2 == 1) {
            result = result * base % m
        }
        base = base * base % m
        exp = exp / 2
    }
    return result
}
