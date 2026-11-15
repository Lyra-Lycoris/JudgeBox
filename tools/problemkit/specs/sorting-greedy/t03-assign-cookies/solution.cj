package t03_assign_cookies

import std.sort.*

func solve(n: Int64, g: Array<Int64>, m: Int64, s: Array<Int64>): Int64 {
    let gg = g.clone()
    let ss = s.clone()
    sort(gg)
    sort(ss)
    var i = 0
    var j = 0
    while (i < n && j < m) {
        if (ss[j] >= gg[i]) {
            i += 1
        }
        j += 1
    }
    return i
}
