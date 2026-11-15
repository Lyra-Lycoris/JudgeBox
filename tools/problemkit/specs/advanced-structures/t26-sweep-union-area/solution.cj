package t26_sweep_union_area

import std.sort.*

func sweepLowerBound(arr: Array<Int64>, len: Int64, x: Int64): Int64 {
    var lo: Int64 = 0
    var hi = len
    while (lo < hi) {
        let mid = lo + (hi - lo) / 2
        if (arr[mid] < x) {
            lo = mid + 1
        } else {
            hi = mid
        }
    }
    return lo
}

func sweepUpdate(node: Int64, left: Int64, right: Int64, ql: Int64, qr: Int64, delta: Int64,
                 cover: Array<Int64>, seglen: Array<Int64>, ys: Array<Int64>): Unit {
    if (!(qr <= left || right <= ql)) {
        if (ql <= left && right <= qr) {
            cover[node] = cover[node] + delta
        } else {
            let mid = (left + right) / 2
            sweepUpdate(node * 2, left, mid, ql, qr, delta, cover, seglen, ys)
            sweepUpdate(node * 2 + 1, mid, right, ql, qr, delta, cover, seglen, ys)
        }
        if (cover[node] > 0) {
            seglen[node] = ys[right] - ys[left]
        } else if (right - left == 1) {
            seglen[node] = 0
        } else {
            seglen[node] = seglen[node * 2] + seglen[node * 2 + 1]
        }
    }
}

func solve(n: Int64, rects: Array<Array<Int64>>): Int64 {
    let totalEvents = 2 * n
    let off: Int64 = 1000000001
    let base = totalEvents + 1
    let keys = Array<Int64>(totalEvents, repeat: 0)
    let eY1 = Array<Int64>(totalEvents, repeat: 0)
    let eY2 = Array<Int64>(totalEvents, repeat: 0)
    let ysAll = Array<Int64>(totalEvents, repeat: 0)
    var idx: Int64 = 0
    var yc: Int64 = 0
    for (i in 0..n) {
        let x1 = rects[i][0]
        let y1 = rects[i][1]
        let x2 = rects[i][2]
        let y2 = rects[i][3]
        keys[idx] = ((x1 + off) * 2) * base + idx
        eY1[idx] = y1
        eY2[idx] = y2
        idx += 1
        keys[idx] = ((x2 + off) * 2 + 1) * base + idx
        eY1[idx] = y1
        eY2[idx] = y2
        idx += 1
        ysAll[yc] = y1
        yc += 1
        ysAll[yc] = y2
        yc += 1
    }
    sort(keys)
    sort(ysAll)

    var k: Int64 = 0
    for (i in 0..yc) {
        if (i == 0 || ysAll[i] != ysAll[i - 1]) {
            ysAll[k] = ysAll[i]
            k += 1
        }
    }

    let cover = Array<Int64>(4 * k + 8, repeat: 0)
    let seglen = Array<Int64>(4 * k + 8, repeat: 0)

    var total: Int64 = 0
    var previous = (keys[0] / base) / 2 - off
    for (t in 0..totalEvents) {
        let rest = keys[t] / base
        let e = keys[t] % base
        let typ = rest % 2
        let x = rest / 2 - off
        total += (x - previous) * seglen[1]
        let ql = sweepLowerBound(ysAll, k, eY1[e])
        let qr = sweepLowerBound(ysAll, k, eY2[e])
        var delta: Int64 = -1
        if (typ == 0) {
            delta = 1
        }
        sweepUpdate(1, 0, k - 1, ql, qr, delta, cover, seglen, ysAll)
        previous = x
    }
    return total
}
