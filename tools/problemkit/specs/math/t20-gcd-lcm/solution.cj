package t20_gcd_lcm

func solve(a: Int64, b: Int64): Array<Int64> {
    var x = a
    var y = b
    while (y != 0) {
        let t = x % y
        x = y
        y = t
    }
    if (x == 0) {
        return [0, 0]
    }
    return [x, a / x * b]
}
