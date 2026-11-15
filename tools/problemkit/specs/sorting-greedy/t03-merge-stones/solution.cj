package t03_merge_stones

import std.sort.*

func solve(n: Int64, a: Array<Int64>): Int64 {
    if (n <= 1) {
        return 0
    }
    let sorted = a.clone()
    sort(sorted)
    let merged = Array<Int64>(n, repeat: 0)
    var ai = 0
    var qh = 0
    var qt = 0
    var total = 0
    for (_ in 1..n) {
        var first = 0
        if (ai < n && (qh >= qt || sorted[ai] <= merged[qh])) {
            first = sorted[ai]
            ai += 1
        } else {
            first = merged[qh]
            qh += 1
        }
        var second = 0
        if (ai < n && (qh >= qt || sorted[ai] <= merged[qh])) {
            second = sorted[ai]
            ai += 1
        } else {
            second = merged[qh]
            qh += 1
        }
        let sum = first + second
        merged[qt] = sum
        qt += 1
        total += sum
    }
    return total
}
