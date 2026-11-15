package t11_inversion_pairs

import std.sort.*

func solve(n: Int64, a: Array<Int64>): Int64 {
    let values = a.clone()
    sort(values)
    var m: Int64 = 0
    for (i in 0..n) {
        if (i == 0 || values[i] != values[i - 1]) {
            values[m] = values[i]
            m += 1
        }
    }
    let tree = Array<Int64>(m + 1, repeat: 0)
    var answer: Int64 = 0
    for (k in 0..n) {
        let x = a[k]
        var lo: Int64 = 0
        var hi: Int64 = m
        while (lo < hi) {
            let mid = lo + (hi - lo) / 2
            if (values[mid] < x) {
                lo = mid + 1
            } else {
                hi = mid
            }
        }
        let p = lo + 1
        var notGreater: Int64 = 0
        var i = p
        while (i > 0) {
            notGreater = notGreater + tree[i]
            i = i - (i & -i)
        }
        answer = answer + k - notGreater
        i = p
        while (i <= m) {
            tree[i] = tree[i] + 1
            i = i + (i & -i)
        }
    }
    return answer
}
