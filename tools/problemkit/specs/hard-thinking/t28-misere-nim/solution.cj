package t28_misere_nim

func solve(n: Int64, a: Array<Int64>): Bool {
    var x: Int64 = 0
    var allOne = true
    for (v in a) {
        x = x ^ v
        if (v != 1) {
            allOne = false
        }
    }
    if (allOne) {
        return n % 2 == 0
    }
    return x != 0
}
