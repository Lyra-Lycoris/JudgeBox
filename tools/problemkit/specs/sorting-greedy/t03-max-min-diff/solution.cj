package t03_max_min_diff

import std.sort.*

func solve(n: Int64, a: Array<Int64>, k: Int64): Int64 {
    if (k <= 1) {
        return 0
    }
    let b = a.clone()
    sort(b)
    var lo = 0
    var hi = (b[n - 1] - b[0]) / (k - 1)
    while (lo < hi) {
        let mid = (lo + hi + 1) / 2
        var cnt = 1
        var last = b[0]
        for (i in 1..n) {
            if (b[i] - last >= mid) {
                cnt += 1
                last = b[i]
                if (cnt >= k) {
                    break
                }
            }
        }
        if (cnt >= k) {
            lo = mid
        } else {
            hi = mid - 1
        }
    }
    return lo
}
