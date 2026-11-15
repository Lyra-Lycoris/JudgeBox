package t07_longest_consecutive

import std.collection.*

func solve(n: Int64, a: Array<Int64>): Int64 {
    let present = HashSet<Int64>()
    for (x in a) {
        present.add(x)
    }
    var best = 0
    for (x in a) {
        if (present.contains(x - 1)) {
            continue
        }
        var y = x
        while (present.contains(y + 1)) {
            y += 1
        }
        if (y - x + 1 > best) {
            best = y - x + 1
        }
    }
    return best
}
