package t28_weighted_interval

import std.sort.*

struct Segment {
    Segment(let r: Int64, let l: Int64, let w: Int64) {}
}

func segmentLess(a: Segment, b: Segment): Ordering {
    if (a.r < b.r) {
        return Ordering.LT
    }
    if (a.r > b.r) {
        return Ordering.GT
    }
    if (a.l < b.l) {
        return Ordering.LT
    }
    if (a.l > b.l) {
        return Ordering.GT
    }
    return Ordering.EQ
}

func solve(n: Int64, seg: Array<Array<Int64>>): Int64 {
    let items = Array<Segment>(n) { i => Segment(seg[i][1], seg[i][0], seg[i][2]) }
    sort(items, by: segmentLess)
    let ends = Array<Int64>(n, repeat: 0)
    for (i in 0..n) {
        ends[i] = items[i].r
    }
    let dp = Array<Int64>(n + 1, repeat: 0)
    for (i in 0..n) {
        let l = items[i].l
        let w = items[i].w
        var lo: Int64 = 0
        var hi = n
        while (lo < hi) {
            let mid = (lo + hi) / 2
            if (ends[mid] < l) {
                lo = mid + 1
            } else {
                hi = mid
            }
        }
        let best = dp[lo] + w
        if (dp[i] > best) {
            dp[i + 1] = dp[i]
        } else {
            dp[i + 1] = best
        }
    }
    return dp[n]
}
