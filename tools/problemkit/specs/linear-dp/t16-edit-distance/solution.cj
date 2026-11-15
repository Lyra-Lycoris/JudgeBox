package t16_edit_distance

func solve(s: String, t: String): Int64 {
    let n = s.size
    let m = t.size
    var prev = Array<Int64>(m + 1, {i => i})
    var cur = Array<Int64>(m + 1, repeat: 0)
    for (i in 1..=n) {
        cur[0] = i
        for (j in 1..=m) {
            var best = prev[j] + 1
            if (cur[j - 1] + 1 < best) {
                best = cur[j - 1] + 1
            }
            var sub = prev[j - 1]
            if (s[i - 1] != t[j - 1]) {
                sub += 1
            }
            if (sub < best) {
                best = sub
            }
            cur[j] = best
        }
        let tmp = prev
        prev = cur
        cur = tmp
    }
    return prev[m]
}
