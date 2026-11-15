package t11_max_subarray_updates

func solve(n: Int64, a: Array<Int64>, q: Int64, ops: Array<Array<Int64>>): Array<Int64> {
    let NEG: Int64 = -(1 << 61)
    var size: Int64 = 1
    while (size < n) {
        size = size << 1
    }

    let total = Array<Int64>(size << 1, repeat: 0)
    let pref = Array<Int64>(size << 1, repeat: NEG)
    let suff = Array<Int64>(size << 1, repeat: NEG)
    let best = Array<Int64>(size << 1, repeat: NEG)
    for (i in 0..n) {
        let k = size + i
        let v = a[i]
        total[k] = v
        pref[k] = v
        suff[k] = v
        best[k] = v
    }
    var k = size - 1
    while (k > 0) {
        let lc = k << 1
        let rc = lc | 1
        total[k] = total[lc] + total[rc]
        var x = pref[lc]
        let y1 = total[lc] + pref[rc]
        if (y1 > x) {
            x = y1
        }
        pref[k] = x
        x = suff[rc]
        let y2 = total[rc] + suff[lc]
        if (y2 > x) {
            x = y2
        }
        suff[k] = x
        var b = best[lc]
        if (best[rc] > b) {
            b = best[rc]
        }
        let cross = suff[lc] + pref[rc]
        if (cross > b) {
            b = cross
        }
        best[k] = b
        k = k - 1
    }

    var queryCount: Int64 = 0
    for (j in 0..q) {
        if (ops[j][0] == 2) {
            queryCount += 1
        }
    }
    let answer = Array<Int64>(queryCount, repeat: 0)
    var written: Int64 = 0
    for (j in 0..q) {
        let t = ops[j][0]
        let px = ops[j][1]
        let py = ops[j][2]
        if (t == 1) {
            var pos = size + px - 1
            total[pos] = py
            pref[pos] = py
            suff[pos] = py
            best[pos] = py
            pos = pos >> 1
            while (pos > 0) {
                let lc = pos << 1
                let rc = lc | 1
                total[pos] = total[lc] + total[rc]
                var p1 = pref[lc]
                let alt1 = total[lc] + pref[rc]
                if (alt1 > p1) {
                    p1 = alt1
                }
                pref[pos] = p1
                var s1 = suff[rc]
                let alt2 = total[rc] + suff[lc]
                if (alt2 > s1) {
                    s1 = alt2
                }
                suff[pos] = s1
                var b1 = best[lc]
                if (best[rc] > b1) {
                    b1 = best[rc]
                }
                let cross1 = suff[lc] + pref[rc]
                if (cross1 > b1) {
                    b1 = cross1
                }
                best[pos] = b1
                pos = pos >> 1
            }
        } else {
            var l = size + px - 1
            var r = size + py
            var ls: Int64 = 0
            var lp: Int64 = NEG
            var lsf: Int64 = NEG
            var lb: Int64 = NEG
            var rs: Int64 = 0
            var rp: Int64 = NEG
            var rsf: Int64 = NEG
            var rb: Int64 = NEG
            while (l < r) {
                if ((l & 1) == 1) {
                    let ns = ls + total[l]
                    var np = lp
                    let alt1 = ls + pref[l]
                    if (alt1 > np) {
                        np = alt1
                    }
                    var nsf = suff[l]
                    let alt2 = total[l] + lsf
                    if (alt2 > nsf) {
                        nsf = alt2
                    }
                    var nb = lb
                    if (best[l] > nb) {
                        nb = best[l]
                    }
                    let cross = lsf + pref[l]
                    if (cross > nb) {
                        nb = cross
                    }
                    ls = ns
                    lp = np
                    lsf = nsf
                    lb = nb
                    l = l + 1
                }
                if ((r & 1) == 1) {
                    r = r - 1
                    let ns = total[r] + rs
                    var np = pref[r]
                    let alt1 = total[r] + rp
                    if (alt1 > np) {
                        np = alt1
                    }
                    var nsf = rsf
                    let alt2 = rs + suff[r]
                    if (alt2 > nsf) {
                        nsf = alt2
                    }
                    var nb = best[r]
                    if (rb > nb) {
                        nb = rb
                    }
                    let cross = suff[r] + rp
                    if (cross > nb) {
                        nb = cross
                    }
                    rs = ns
                    rp = np
                    rsf = nsf
                    rb = nb
                }
                l = l >> 1
                r = r >> 1
            }
            var result = lb
            if (rb > result) {
                result = rb
            }
            let crossFinal = lsf + rp
            if (crossFinal > result) {
                result = crossFinal
            }
            answer[written] = result
            written += 1
        }
    }
    return answer
}
