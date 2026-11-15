package t26_range_add_range_sum

func solve(n: Int64, a: Array<Int64>, q: Int64, ops: Array<Array<Int64>>): Array<Int64> {
    let b1 = Array<Int64>(n + 2, repeat: 0)
    let b2 = Array<Int64>(n + 2, repeat: 0)
    for (i in 1..(n + 1)) {
        let v = a[i - 1]
        b1[i] = v
        b2[i] = v * (i - 1)
    }
    for (i in 1..(n + 1)) {
        let j = i + (i & -i)
        if (j <= n) {
            b1[j] = b1[j] + b1[i]
            b2[j] = b2[j] + b2[i]
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
        let l = ops[k][1]
        let r = ops[k][2]
        let x = ops[k][3]
        if (t == 1) {
            let m1 = x * (l - 1)
            let m2 = x * r
            var i = l
            while (i <= n) {
                b1[i] = b1[i] + x
                b2[i] = b2[i] + m1
                i = i + (i & -i)
            }
            i = r + 1
            while (i <= n) {
                b1[i] = b1[i] - x
                b2[i] = b2[i] - m2
                i = i + (i & -i)
            }
        } else {
            var total: Int64 = 0
            var i = r
            while (i > 0) {
                total = total + b1[i] * r - b2[i]
                i = i - (i & -i)
            }
            i = l - 1
            while (i > 0) {
                total = total - (b1[i] * (l - 1) - b2[i])
                i = i - (i & -i)
            }
            answer[written] = total
            written += 1
        }
    }
    return answer
}
