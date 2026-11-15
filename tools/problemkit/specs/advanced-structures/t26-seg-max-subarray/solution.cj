package t26_seg_max_subarray

func solve(n: Int64, a: Array<Int64>, q: Int64, ops: Array<Array<Int64>>): Array<Int64> {
    let NEG: Int64 = -(1 << 61)
    var size: Int64 = 1
    while (size < n) {
        size = size << 1
    }

    let total = Array<Int64>(size << 1, repeat: 0)
    let pre = Array<Int64>(size << 1, repeat: NEG)
    let suf = Array<Int64>(size << 1, repeat: NEG)
    let bst = Array<Int64>(size << 1, repeat: NEG)
    for (i in 0..n) {
        let k = size + i
        let v = a[i]
        total[k] = v
        pre[k] = v
        suf[k] = v
        bst[k] = v
    }
    var k = size - 1
    while (k > 0) {
        let lc = k << 1
        let rc = lc | 1
        total[k] = total[lc] + total[rc]
        var x = pre[lc]
        let alt1 = total[lc] + pre[rc]
        if (alt1 > x) {
            x = alt1
        }
        pre[k] = x
        x = suf[rc]
        let alt2 = total[rc] + suf[lc]
        if (alt2 > x) {
            x = alt2
        }
        suf[k] = x
        x = bst[lc]
        if (bst[rc] > x) {
            x = bst[rc]
        }
        let cross0 = suf[lc] + pre[rc]
        if (cross0 > x) {
            x = cross0
        }
        bst[k] = x
        k = k - 1
    }

    let answer = Array<Int64>(q, repeat: 0)
    for (j in 0..q) {
        var l = size + ops[j][0] - 1
        var r = size + ops[j][1]
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
                let alt1 = ls + pre[l]
                if (alt1 > np) {
                    np = alt1
                }
                var nsf = suf[l]
                let alt2 = total[l] + lsf
                if (alt2 > nsf) {
                    nsf = alt2
                }
                var nb = lb
                if (bst[l] > nb) {
                    nb = bst[l]
                }
                let c1 = lsf + pre[l]
                if (c1 > nb) {
                    nb = c1
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
                var np = pre[r]
                let alt1 = total[r] + rp
                if (alt1 > np) {
                    np = alt1
                }
                var nsf = rs + suf[r]
                if (rsf > nsf) {
                    nsf = rsf
                }
                var nb = bst[r]
                if (rb > nb) {
                    nb = rb
                }
                let c1 = suf[r] + rp
                if (c1 > nb) {
                    nb = c1
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
        let cFinal = lsf + rp
        if (cFinal > result) {
            result = cFinal
        }
        answer[j] = result
    }
    return answer
}
