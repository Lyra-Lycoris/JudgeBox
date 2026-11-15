package t12_least_rotation

func solve(n: Int64, s: String): Int64 {
    let chars = s.toRuneArray()
    let m = chars.size
    if (m <= 1) {
        return 0
    }
    let doubled = Array<Rune>(2 * m, repeat: r'a')
    for (index in 0..m) {
        doubled[index] = chars[index]
        doubled[index + m] = chars[index]
    }
    var i: Int64 = 0
    var j: Int64 = 1
    var k: Int64 = 0
    while (i < m && j < m && k < m) {
        let a = doubled[i + k]
        let b = doubled[j + k]
        if (a == b) {
            k += 1
        } else if (UInt32(a) > UInt32(b)) {
            i = i + k + 1
            if (i <= j) {
                i = j + 1
            }
            k = 0
        } else {
            j = j + k + 1
            if (j <= i) {
                j = i + 1
            }
            k = 0
        }
    }
    if (i < j) {
        return i
    }
    return j
}
