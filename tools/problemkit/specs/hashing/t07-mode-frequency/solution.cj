package t07_mode_frequency

import std.collection.*

func solve(n: Int64, a: Array<Int64>): Int64 {
    let counts = HashMap<Int64, Int64>()
    var best = 0
    for (x in a) {
        var current = 1
        if (counts.contains(x)) {
            current = counts[x] + 1
        }
        counts[x] = current
        if (current > best) {
            best = current
        }
    }
    return best
}
