package t11_kth_smallest_dynamic

import std.sort.*

func solve(q: Int64, ops: Array<Array<Int64>>): Array<Int64> {
    var insertCount: Int64 = 0
    for (j in 0..q) {
        if (ops[j][0] == 1) {
            insertCount += 1
        }
    }
    let values = Array<Int64>(insertCount, repeat: 0)
    var at: Int64 = 0
    for (j in 0..q) {
        if (ops[j][0] == 1) {
            values[at] = ops[j][1]
            at += 1
        }
    }
    sort(values)
    var m: Int64 = 0
    for (i in 0..insertCount) {
        if (i == 0 || values[i] != values[i - 1]) {
            values[m] = values[i]
            m += 1
        }
    }
    let tree = Array<Int64>(m + 1, repeat: 0)
    var highest: Int64 = 0
    while ((1 << (highest + 1)) <= m) {
        highest += 1
    }
    var step0: Int64 = 0
    if (m > 0) {
        step0 = 1 << highest
    }

    var queryCount: Int64 = 0
    for (j in 0..q) {
        if (ops[j][0] == 3) {
            queryCount += 1
        }
    }
    let answer = Array<Int64>(queryCount, repeat: 0)
    var written: Int64 = 0
    for (j in 0..q) {
        let t = ops[j][0]
        let x = ops[j][1]
        if (t == 1 || t == 2) {
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
            var i = lo + 1
            var delta: Int64 = 1
            if (t == 2) {
                delta = -1
            }
            while (i <= m) {
                tree[i] = tree[i] + delta
                i = i + (i & -i)
            }
        } else {
            var k = x
            var pos: Int64 = 0
            var step = step0
            while (step > 0) {
                let nxt = pos + step
                if (nxt <= m && tree[nxt] < k) {
                    pos = nxt
                    k = k - tree[nxt]
                }
                step = step >> 1
            }
            answer[written] = values[pos]
            written += 1
        }
    }
    return answer
}
