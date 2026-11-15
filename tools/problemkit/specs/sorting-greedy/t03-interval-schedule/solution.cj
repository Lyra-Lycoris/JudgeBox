package t03_interval_schedule

import std.sort.*

func solve(n: Int64, l: Array<Int64>, r: Array<Int64>): Int64 {
    let shift = 1000000000
    let base = 2000000001
    let keys = Array<Int64>(n, repeat: 0)
    for (i in 0..n) {
        keys[i] = (r[i] + shift) * base + (l[i] + shift)
    }
    sort(keys)
    var answer = 0
    var lastEnd = -1152921504606846976
    for (i in 0..n) {
        let li = keys[i] % base - shift
        let ri = keys[i] / base - shift
        if (li >= lastEnd) {
            answer += 1
            lastEnd = ri
        }
    }
    return answer
}
