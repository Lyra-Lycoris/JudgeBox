package t11_distinct_in_range

import std.sort.*

func solve(n: Int64, a: Array<Int64>, q: Int64, queries: Array<Array<Int64>>): Array<Int64> {
    let values = a.clone()
    sort(values)
    var m: Int64 = 0
    for (i in 0..n) {
        if (i == 0 || values[i] != values[i - 1]) {
            values[m] = values[i]
            m += 1
        }
    }
    let last = Array<Int64>(m + 1, repeat: 0)

    let head = Array<Int64>(n + 1, repeat: -1)
    let nxt = Array<Int64>(q, repeat: -1)
    for (j in 0..q) {
        let r = queries[j][1]
        nxt[j] = head[r]
        head[r] = j
    }

    let tree = Array<Int64>(n + 1, repeat: 0)
    let answer = Array<Int64>(q, repeat: 0)

    for (r in 1..n + 1) {
        let x = a[r - 1]
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
        let id = lo + 1
        if (last[id] != 0) {
            var i = last[id]
            while (i <= n) {
                tree[i] = tree[i] - 1
                i = i + (i & -i)
            }
        }
        last[id] = r
        var i = r
        while (i <= n) {
            tree[i] = tree[i] + 1
            i = i + (i & -i)
        }

        var upto: Int64 = 0
        i = r
        while (i > 0) {
            upto = upto + tree[i]
            i = i - (i & -i)
        }

        var j = head[r]
        while (j != -1) {
            var s: Int64 = 0
            i = queries[j][0] - 1
            while (i > 0) {
                s = s + tree[i]
                i = i - (i & -i)
            }
            answer[j] = upto - s
            j = nxt[j]
        }
    }
    return answer
}
