package t03_meeting_rooms

import std.sort.*

func solve(n: Int64, s: Array<Int64>, e: Array<Int64>): Int64 {
    let ss = s.clone()
    let ee = e.clone()
    sort(ss)
    sort(ee)
    var i = 0
    var j = 0
    var cur = 0
    var best = 0
    while (i < n) {
        if (ss[i] < ee[j]) {
            cur += 1
            if (cur > best) {
                best = cur
            }
            i += 1
        } else {
            cur -= 1
            j += 1
        }
    }
    return best
}
