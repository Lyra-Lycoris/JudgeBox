package t18_king_placement

import std.collection.*

func solve(n: Int64, m: Int64): Int64 {
    var rows = n
    var cols = m
    if (rows < cols) {
        let t = rows
        rows = cols
        cols = t
    }
    let size: Int64 = 1 << cols
    let valid = ArrayList<Int64>()
    var mask: Int64 = 0
    while (mask < size) {
        if ((mask & (mask << 1)) == 0) {
            valid.add(mask)
        }
        mask += 1
    }
    let dp = Array<Int64>(size, repeat: 0)
    let ndp = Array<Int64>(size, repeat: 0)
    for (a in valid) {
        dp[a] = 1
    }
    var r: Int64 = 1
    while (r < rows) {
        for (a in valid) {
            var sum: Int64 = 0
            for (b in valid) {
                if ((a & b) == 0 && (a & (b << 1)) == 0 && ((a << 1) & b) == 0) {
                    sum += dp[b]
                }
            }
            ndp[a] = sum
        }
        for (a in valid) {
            dp[a] = ndp[a]
        }
        r += 1
    }
    var total: Int64 = 0
    for (a in valid) {
        total += dp[a]
    }
    return total
}
