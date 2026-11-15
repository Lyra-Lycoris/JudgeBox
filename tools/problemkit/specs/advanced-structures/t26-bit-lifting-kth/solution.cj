package t26_bit_lifting_kth

func solve(n: Int64, a: Array<Int64>, q: Int64, ops: Array<Array<Int64>>): Array<Int64> {
    let cur = Array<Int64>(n, repeat: 0)
    for (i in 0..n) {
        cur[i] = a[i]
    }
    let bit = Array<Int64>(n + 1, repeat: 0)
    for (i in 1..(n + 1)) {
        bit[i] = bit[i] + cur[i - 1]
        let j = i + (i & -i)
        if (j <= n) {
            bit[j] = bit[j] + bit[i]
        }
    }

    var step0: Int64 = 1
    while ((step0 << 1) <= n) {
        step0 = step0 << 1
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
        let v = ops[k][2]
        if (t == 1) {
            let delta = v - cur[x - 1]
            cur[x - 1] = v
            var i = x
            while (i <= n) {
                bit[i] = bit[i] + delta
                i = i + (i & -i)
            }
        } else {
            var need = x
            var pos: Int64 = 0
            var step = step0
            while (step > 0) {
                let nxt = pos + step
                if (nxt <= n && bit[nxt] < need) {
                    pos = nxt
                    need = need - bit[nxt]
                }
                step = step >> 1
            }
            answer[written] = pos + 1
            written += 1
        }
    }
    return answer
}
