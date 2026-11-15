package t12_min_period

func solve(n: Int64, s: String): Int64 {
    let chars = s.toRuneArray()
    let m = chars.size
    if (m <= 0) {
        return 0
    }
    let pi = Array<Int64>(m, repeat: 0)
    for (i in 1..m) {
        var k = pi[i - 1]
        while (k > 0 && chars[i] != chars[k]) {
            k = pi[k - 1]
        }
        if (chars[i] == chars[k]) {
            k += 1
        }
        pi[i] = k
    }
    let d = m - pi[m - 1]
    if (m % d == 0) {
        return d
    }
    return m
}
