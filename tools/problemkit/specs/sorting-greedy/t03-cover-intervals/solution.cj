package t03_cover_intervals

import std.sort.*

func solve(n: Int64, l: Array<Int64>, r: Array<Int64>, m: Int64): Int64 {
    let shift = 1000000000
    let base = 2000000001
    let keys = Array<Int64>(n, repeat: 0)
    for (i in 0..n) {
        keys[i] = (l[i] + shift) * base + (r[i] + shift)
    }
    sort(keys)
    var i = 0
    var cur = 0
    var count = 0
    while (cur < m) {
        var best = -1
        while (i < n && keys[i] / base - shift <= cur) {
            let rr = keys[i] % base - shift
            if (rr > best) {
                best = rr
            }
            i += 1
        }
        if (best <= cur) {
            return -1
        }
        cur = best
        count += 1
    }
    return count
}
