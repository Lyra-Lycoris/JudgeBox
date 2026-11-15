package t27_king_placement_mask

func solve(n: Int64, m: Int64, blocked: Array<Int64>): Int64 {
    let MOD: Int64 = 1000000007
    let full: Int64 = 1 << m
    let valid = Array<Int64>(full, repeat: 0)
    var count: Int64 = 0
    var s: Int64 = 0
    while (s < full) {
        if ((s & (s << 1)) == 0) {
            valid[count] = s
            count += 1
        }
        s += 1
    }
    let compat = Array<Int64>(full * count, repeat: 0)
    var i: Int64 = 0
    while (i < count) {
        let a = valid[i]
        var j: Int64 = 0
        while (j < count) {
            let b = valid[j]
            if ((a & b) == 0 && ((a << 1) & b) == 0 && ((a >> 1) & b) == 0) {
                compat[i * count + j] = 1
            }
            j += 1
        }
        i += 1
    }
    let dp = Array<Int64>(full, repeat: 0)
    let b0 = blocked[0]
    i = 0
    while (i < count) {
        let a = valid[i]
        if ((a & b0) == 0) {
            dp[a] = 1
        }
        i += 1
    }
    var row: Int64 = 1
    while (row < n) {
        let b = blocked[row]
        let ndp = Array<Int64>(full, repeat: 0)
        i = 0
        while (i < count) {
            let a = valid[i]
            if ((a & b) == 0) {
                var total: Int64 = 0
                let base = i * count
                var j: Int64 = 0
                while (j < count) {
                    if (compat[base + j] == 1) {
                        total += dp[valid[j]]
                    }
                    j += 1
                }
                ndp[a] = total % MOD
            }
            i += 1
        }
        var k: Int64 = 0
        while (k < full) {
            dp[k] = ndp[k]
            k += 1
        }
        row += 1
    }
    var ans: Int64 = 0
    i = 0
    while (i < count) {
        ans += dp[valid[i]]
        i += 1
    }
    return ans % MOD
}
