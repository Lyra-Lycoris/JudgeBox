package t04_two_array_pairs

import std.sort.*

func solve(n: Int64, a: Array<Int64>, m: Int64, b: Array<Int64>, x: Int64): Int64 {
    let c = b.clone()
    sort(c)
    var ans = 0
    for (v in a) {
        let need = x - v
        var lo = 0
        var hi = m
        while (lo < hi) {
            let mid = lo + (hi - lo) / 2
            if (c[mid] <= need) {
                lo = mid + 1
            } else {
                hi = mid
            }
        }
        ans += lo
    }
    return ans
}
