package t07_two_sum_exists

import std.collection.*

func solve(n: Int64, a: Array<Int64>, target: Int64): Bool {
    let seen = HashSet<Int64>()
    for (x in a) {
        if (seen.contains(target - x)) {
            return true
        }
        seen.add(x)
    }
    return false
}
