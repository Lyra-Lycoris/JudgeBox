package t28_adjacent_swap_sort

import std.sort.*

func solve(n: Int64, a: Array<Int64>): Int64 {
    let keys = Array<Int64>(n, repeat: 0)
    for (i in 0..n) {
        keys[i] = (a[i] + 1000000000) * 1000000 + i
    }
    sort(keys)
    let bit = Array<Int64>(n + 1, repeat: 0)
    var answer: Int64 = 0
    var seen: Int64 = 0
    for (k in 0..n) {
        let pos = keys[k] % 1000000 + 1
        var s: Int64 = 0
        var t = pos
        while (t > 0) {
            s += bit[t]
            t -= t & (-t)
        }
        answer += seen - s
        seen += 1
        t = pos
        while (t <= n) {
            bit[t] += 1
            t += t & (-t)
        }
    }
    return answer
}
