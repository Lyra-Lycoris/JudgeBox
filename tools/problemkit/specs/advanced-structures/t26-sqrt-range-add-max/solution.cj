package t26_sqrt_range_add_max

func solve(n: Int64, a: Array<Int64>, q: Int64, ops: Array<Array<Int64>>): Array<Int64> {
    let NEG: Int64 = -(1 << 62)
    var blockSize: Int64 = 1
    while (blockSize * blockSize < n) {
        blockSize += 1
    }
    blockSize += 1
    let blocks = (n + blockSize - 1) / blockSize

    let val = Array<Int64>(n, repeat: 0)
    for (i in 0..n) {
        val[i] = a[i]
    }
    let lazy = Array<Int64>(blocks, repeat: 0)
    let best = Array<Int64>(blocks, repeat: NEG)
    for (i in 0..n) {
        let b = i / blockSize
        if (val[i] > best[b]) {
            best[b] = val[i]
        }
    }

    var queryCount: Int64 = 0
    for (k in 0..q) {
        if (ops[k][0] == 2) {
            queryCount += 1
        }
    }
    let answer = Array<Int64>(queryCount, repeat: 0)
    var written: Int64 = 0
    for (k in 0..q) {
        let t = ops[k][0]
        let l = ops[k][1] - 1
        let r = ops[k][2] - 1
        let x = ops[k][3]
        let bl = l / blockSize
        let br = r / blockSize
        if (t == 1) {
            if (bl == br) {
                var i = l
                while (i <= r) {
                    val[i] = val[i] + x
                    i += 1
                }
                var m = NEG
                var hi = (bl + 1) * blockSize
                if (hi > n) {
                    hi = n
                }
                i = bl * blockSize
                while (i < hi) {
                    if (val[i] > m) {
                        m = val[i]
                    }
                    i += 1
                }
                best[bl] = m
            } else {
                var i = l
                while (i < (bl + 1) * blockSize) {
                    val[i] = val[i] + x
                    i += 1
                }
                var m = NEG
                i = bl * blockSize
                while (i < (bl + 1) * blockSize) {
                    if (val[i] > m) {
                        m = val[i]
                    }
                    i += 1
                }
                best[bl] = m
                i = br * blockSize
                while (i <= r) {
                    val[i] = val[i] + x
                    i += 1
                }
                m = NEG
                var hi = (br + 1) * blockSize
                if (hi > n) {
                    hi = n
                }
                i = br * blockSize
                while (i < hi) {
                    if (val[i] > m) {
                        m = val[i]
                    }
                    i += 1
                }
                best[br] = m
                var b = bl + 1
                while (b < br) {
                    lazy[b] = lazy[b] + x
                    b += 1
                }
            }
        } else {
            var m = NEG
            if (bl == br) {
                var i = l
                while (i <= r) {
                    let v = val[i] + lazy[bl]
                    if (v > m) {
                        m = v
                    }
                    i += 1
                }
            } else {
                var i = l
                while (i < (bl + 1) * blockSize) {
                    let v = val[i] + lazy[bl]
                    if (v > m) {
                        m = v
                    }
                    i += 1
                }
                i = br * blockSize
                while (i <= r) {
                    let v = val[i] + lazy[br]
                    if (v > m) {
                        m = v
                    }
                    i += 1
                }
                var b = bl + 1
                while (b < br) {
                    let v = best[b] + lazy[b]
                    if (v > m) {
                        m = v
                    }
                    b += 1
                }
            }
            answer[written] = m
            written += 1
        }
    }
    return answer
}
