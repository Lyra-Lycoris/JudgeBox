package t27_reroot_eccentricity

func solve(n: Int64, p: Array<Int64>): Array<Int64> {
    let down = Array<Int64>(n + 1, repeat: 0)
    let up = Array<Int64>(n + 1, repeat: 0)
    let best1 = Array<Int64>(n + 1, repeat: 0)
    let best2 = Array<Int64>(n + 1, repeat: 0)
    let who = Array<Int64>(n + 1, repeat: 0)
    var i: Int64 = n
    while (i >= 2) {
        let par = p[i - 2]
        let val = down[i] + 1
        if (val > best1[par]) {
            best2[par] = best1[par]
            best1[par] = val
            who[par] = i
        } else if (val > best2[par]) {
            best2[par] = val
        }
        if (val > down[par]) {
            down[par] = val
        }
        i -= 1
    }
    i = 2
    while (i <= n) {
        let par = p[i - 2]
        var sib = best1[par]
        if (who[par] == i) {
            sib = best2[par]
        }
        var base = up[par]
        if (sib > base) {
            base = sib
        }
        up[i] = base + 1
        i += 1
    }
    let ans = Array<Int64>(n, repeat: 0)
    i = 1
    while (i <= n) {
        ans[i - 1] = down[i]
        if (up[i] > ans[i - 1]) {
            ans[i - 1] = up[i]
        }
        i += 1
    }
    return ans
}
