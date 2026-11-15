package t02_max_xor_pair

func solve(n: Int64, a: Array<Int64>): Int64 {
    var best: Int64 = 0
    var i: Int64 = 0
    while (i < n) {
        let ai = a[i]
        var j = i + 1
        while (j < n) {
            let v = ai ^ a[j]
            if (v > best) {
                best = v
            }
            j += 1
        }
        i += 1
    }
    return best
}
