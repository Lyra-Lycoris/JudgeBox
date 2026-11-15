package t02_subset_sum

import std.collection.*

func solve(target: Int64, n: Int64, a: Array<Int64>): Bool {
    let sums = ArrayList<Int64>()
    sums.add(0)
    for (x in a) {
        let m = sums.size
        for (i in 0..m) {
            sums.add(sums[i] + x)
        }
    }
    for (s in sums) {
        if (s == target) {
            return true
        }
    }
    return false
}
