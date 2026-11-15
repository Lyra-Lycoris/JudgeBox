package t06_three_sum_zero_count

import std.sort.*

func solve(n: Int64, a: Array<Int64>): Int64 {
    let b = a.clone()
    sort(b)
    var count: Int64 = 0
    var i: Int64 = 0
    while (i + 2 < n) {
        var lo: Int64 = i + 1
        var hi: Int64 = n - 1
        while (lo < hi) {
            let sum = b[i] + b[lo] + b[hi]
            if (sum < 0) {
                lo += 1
            } else if (sum > 0) {
                hi -= 1
            } else if (b[lo] == b[hi]) {
                let m = hi - lo + 1
                count += m * (m - 1) / 2
                break
            } else {
                var lowCount: Int64 = 1
                while (lo + lowCount < hi && b[lo + lowCount] == b[lo]) {
                    lowCount += 1
                }
                var highCount: Int64 = 1
                while (hi - highCount > lo && b[hi - highCount] == b[hi]) {
                    highCount += 1
                }
                count += lowCount * highCount
                lo += lowCount
                hi -= highCount
            }
        }
        i += 1
    }
    return count
}
