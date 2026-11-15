package t02_triple_zero

import std.sort.*

func solve(n: Int64, a: Array<Int64>): Int64 {
    let v = a.clone()
    sort(v)
    var total: Int64 = 0
    var i: Int64 = 0
    while (i + 2 < n) {
        var l = i + 1
        var r = n - 1
        while (l < r) {
            let s = v[i] + v[l] + v[r]
            if (s == 0) {
                if (v[l] == v[r]) {
                    let c = r - l + 1
                    total += c * (c - 1) / 2
                    break
                }
                var cl: Int64 = 1
                while (l + cl < r && v[l + cl] == v[l]) {
                    cl += 1
                }
                var cr: Int64 = 1
                while (r - cr > l && v[r - cr] == v[r]) {
                    cr += 1
                }
                total += cl * cr
                l += cl
                r -= cr
            } else if (s < 0) {
                l += 1
            } else {
                r -= 1
            }
        }
        i += 1
    }
    return total
}
