package t28_min_cyclic_rotation

func solve(n: Int64, a: Array<Int64>): Array<Int64> {
    var i: Int64 = 0
    var j: Int64 = 1
    var k: Int64 = 0
    while (i < n && j < n && k < n) {
        let x = a[(i + k) % n]
        let y = a[(j + k) % n]
        if (x == y) {
            k += 1
        } else if (x > y) {
            i = i + k + 1
            if (i == j) {
                i += 1
            }
            k = 0
        } else {
            j = j + k + 1
            if (i == j) {
                j += 1
            }
            k = 0
        }
    }
    var s = i
    if (j < s) {
        s = j
    }
    if (s >= n) {
        s = 0
    }
    let result = Array<Int64>(n, repeat: 0)
    for (t in 0..n) {
        result[t] = a[(s + t) % n]
    }
    return result
}
