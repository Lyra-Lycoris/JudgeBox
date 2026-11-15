package t22_subset_xor_sum

func solve(n: Int64, a: Array<Int64>): Int64 {
    let mod: Int64 = 1000000007
    var mask: Int64 = 0
    for (v in a) {
        mask = mask | v
    }
    var base: Int64 = 2
    var exponent = n - 1
    var power: Int64 = 1
    while (exponent > 0) {
        if (exponent % 2 == 1) {
            power = power * base % mod
        }
        base = base * base % mod
        exponent = exponent / 2
    }
    return mask % mod * power % mod
}
