package t26_sqrt_range_mode

import std.sort.*

func modeLowerBoundRange(flat: Array<Int64>, from: Int64, to: Int64, x: Int64): Int64 {
    var lo = from
    var hi = to
    while (lo < hi) {
        let mid = lo + (hi - lo) / 2
        if (flat[mid] < x) {
            lo = mid + 1
        } else {
            hi = mid
        }
    }
    return lo
}

func modeCountIn(flat: Array<Int64>, from: Int64, to: Int64, l: Int64, r: Int64): Int64 {
    let left = modeLowerBoundRange(flat, from, to, l)
    let right = modeLowerBoundRange(flat, from, to, r + 1)
    return right - left
}

func solve(n: Int64, a: Array<Int64>, q: Int64, ops: Array<Array<Int64>>): Array<Int64> {
    let values = a.clone()
    sort(values)
    var m: Int64 = 0
    for (i in 0..n) {
        if (i == 0 || values[i] != values[i - 1]) {
            values[m] = values[i]
            m += 1
        }
    }

    let comp = Array<Int64>(n, repeat: 0)
    for (i in 0..n) {
        let x = a[i]
        var lo: Int64 = 0
        var hi = m
        while (lo < hi) {
            let mid = lo + (hi - lo) / 2
            if (values[mid] < x) {
                lo = mid + 1
            } else {
                hi = mid
            }
        }
        comp[i] = lo
    }

    let cntVals = Array<Int64>(m, repeat: 0)
    for (i in 0..n) {
        let v = comp[i]
        cntVals[v] = cntVals[v] + 1
    }
    let start = Array<Int64>(m + 1, repeat: 0)
    for (v in 0..m) {
        start[v + 1] = start[v] + cntVals[v]
    }
    let cursor = Array<Int64>(m, repeat: 0)
    let flat = Array<Int64>(n, repeat: 0)
    for (i in 0..n) {
        let v = comp[i]
        flat[start[v] + cursor[v]] = i
        cursor[v] = cursor[v] + 1
    }

    var B: Int64 = 1
    while ((B + 1) * (B + 1) <= n) {
        B += 1
    }
    let nb = (n + B - 1) / B
    let tableC = Array<Array<Int64>>(nb, { _ => Array<Int64>(nb, repeat: 0) })
    let tableV = Array<Array<Int64>>(nb, { _ => Array<Int64>(nb, repeat: -1) })
    let cnt = Array<Int64>(m, repeat: 0)
    for (s in 0..nb) {
        for (v in 0..m) {
            cnt[v] = 0
        }
        var bc: Int64 = 0
        var bv: Int64 = -1
        var i = s * B
        while (i < n) {
            let v = comp[i]
            let c = cnt[v] + 1
            cnt[v] = c
            if (c > bc || (c == bc && v < bv)) {
                bc = c
                bv = v
            }
            if ((i + 1) % B == 0 || i == n - 1) {
                tableC[s][i / B] = bc
                tableV[s][i / B] = bv
            }
            i += 1
        }
    }

    let answer = Array<Int64>(q, repeat: 0)
    let cnt2 = Array<Int64>(m, repeat: 0)
    let touched = Array<Int64>(B + 1, repeat: 0)
    for (t in 0..q) {
        let l = ops[t][0] - 1
        let r = ops[t][1] - 1
        let bl = l / B
        let br = r / B
        var bc: Int64 = 0
        var bv: Int64 = -1
        if (bl == br) {
            var nt: Int64 = 0
            var i = l
            while (i <= r) {
                let v = comp[i]
                if (cnt2[v] == 0) {
                    touched[nt] = v
                    nt += 1
                }
                let c = cnt2[v] + 1
                cnt2[v] = c
                if (c > bc || (c == bc && v < bv)) {
                    bc = c
                    bv = v
                }
                i += 1
            }
            var j: Int64 = 0
            while (j < nt) {
                cnt2[touched[j]] = 0
                j += 1
            }
        } else {
            if (bl + 1 < br) {
                bc = tableC[bl + 1][br - 1]
                bv = tableV[bl + 1][br - 1]
            }
            let end = (bl + 1) * B
            var i = l
            while (i < end) {
                let v = comp[i]
                let c = modeCountIn(flat, start[v], start[v + 1], l, r)
                if (c > bc || (c == bc && v < bv)) {
                    bc = c
                    bv = v
                }
                i += 1
            }
            i = br * B
            while (i <= r) {
                let v = comp[i]
                let c = modeCountIn(flat, start[v], start[v + 1], l, r)
                if (c > bc || (c == bc && v < bv)) {
                    bc = c
                    bv = v
                }
                i += 1
            }
        }
        answer[t] = values[bv]
    }
    return answer
}
