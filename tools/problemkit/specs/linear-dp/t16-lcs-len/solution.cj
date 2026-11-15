package t16_lcs_len

func solve(s: String, t: String): Int64 {
    let m = t.size
    var prev = Array<Int64>(m + 1, repeat: 0)
    var cur = Array<Int64>(m + 1, repeat: 0)
    for (i in 1..=s.size) {
        for (j in 1..=m) {
            if (s[i - 1] == t[j - 1]) {
                cur[j] = prev[j - 1] + 1
            } else if (prev[j] >= cur[j - 1]) {
                cur[j] = prev[j]
            } else {
                cur[j] = cur[j - 1]
            }
        }
        let tmp = prev
        prev = cur
        cur = tmp
    }
    return prev[m]
}
