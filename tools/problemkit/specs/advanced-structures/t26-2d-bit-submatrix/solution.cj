package t26_2d_bit_submatrix

func prefixSum2D(bit: Array<Array<Int64>>, x: Int64, y: Int64): Int64 {
    var s: Int64 = 0
    var i = x
    while (i > 0) {
        let bi = bit[i]
        var j = y
        while (j > 0) {
            s = s + bi[j]
            j = j - (j & -j)
        }
        i = i - (i & -i)
    }
    return s
}

func solve(n: Int64, m: Int64, a: Array<Array<Int64>>, q: Int64, ops: Array<Array<Int64>>): Array<Int64> {
    let pre = Array<Array<Int64>>(n + 1, { _ => Array<Int64>(m + 1, repeat: 0) })
    for (i in 1..(n + 1)) {
        var s: Int64 = 0
        let row = a[i - 1]
        let pi = pre[i]
        let pj = pre[i - 1]
        for (j in 1..(m + 1)) {
            s = s + row[j - 1]
            pi[j] = pj[j] + s
        }
    }

    let bit = Array<Array<Int64>>(n + 1, { _ => Array<Int64>(m + 1, repeat: 0) })
    for (i in 1..(n + 1)) {
        let li = i - (i & -i)
        let bi = bit[i]
        let pi = pre[i]
        let pli = pre[li]
        for (j in 1..(m + 1)) {
            let lj = j - (j & -j)
            bi[j] = pi[j] - pli[j] - pi[lj] + pli[lj]
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
        let x = ops[k][1]
        let y = ops[k][2]
        if (t == 1) {
            let v = ops[k][3]
            var i = x
            while (i <= n) {
                let bi = bit[i]
                var j = y
                while (j <= m) {
                    bi[j] = bi[j] + v
                    j = j + (j & -j)
                }
                i = i + (i & -i)
            }
        } else {
            let x2 = ops[k][3]
            let y2 = ops[k][4]
            let s1 = prefixSum2D(bit, x2, y2)
            let s2 = prefixSum2D(bit, x - 1, y2)
            let s3 = prefixSum2D(bit, x2, y - 1)
            let s4 = prefixSum2D(bit, x - 1, y - 1)
            let total = s1 - s2 - s3 + s4
            answer[written] = total
            written += 1
        }
    }
    return answer
}
