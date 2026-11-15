package t12_kmp_count

func solve(n: Int64, s: String, m: Int64, p: String): Int64 {
    let text = s.toRuneArray()
    let pattern = p.toRuneArray()
    if (m <= 0 || m > text.size || m > pattern.size) {
        return 0
    }
    let pi = Array<Int64>(m, repeat: 0)
    var k: Int64 = 0
    for (i in 1..m) {
        while (k > 0 && pattern[i] != pattern[k]) {
            k = pi[k - 1]
        }
        if (pattern[i] == pattern[k]) {
            k += 1
        }
        pi[i] = k
    }
    var count: Int64 = 0
    k = 0
    for (ch in text) {
        while (k > 0 && ch != pattern[k]) {
            k = pi[k - 1]
        }
        if (ch == pattern[k]) {
            k += 1
            if (k == m) {
                count += 1
                k = pi[k - 1]
            }
        }
    }
    return count
}
