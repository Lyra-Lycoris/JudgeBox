package t17_max_expr_value

func solve(m: Int64, nums: Array<Int64>, ops: Array<String>): Int64 {
    let NEG = -4000000000000000000
    let POS = 4000000000000000000
    let mx = Array<Array<Int64>>(m, { _ => Array<Int64>(m, repeat: NEG) })
    let mn = Array<Array<Int64>>(m, { _ => Array<Int64>(m, repeat: POS) })
    for (i in 0..m) {
        mx[i][i] = nums[i]
        mn[i][i] = nums[i]
    }
    for (len in 2..m + 1) {
        for (i in 0..m - len + 1) {
            let j = i + len - 1
            for (k in i..j) {
                let a1 = mx[i][k]
                let a2 = mn[i][k]
                let b1 = mx[k + 1][j]
                let b2 = mn[k + 1][j]
                let op = ops[k]
                let cand = Array<Int64>(4, repeat: 0)
                var cnt = 0
                if (op == "+") {
                    cand[0] = a1 + b1
                    cand[1] = a2 + b2
                    cnt = 2
                } else if (op == "-") {
                    cand[0] = a1 - b2
                    cand[1] = a2 - b1
                    cnt = 2
                } else {
                    cand[0] = a1 * b1
                    cand[1] = a1 * b2
                    cand[2] = a2 * b1
                    cand[3] = a2 * b2
                    cnt = 4
                }
                for (t in 0..cnt) {
                    if (cand[t] > mx[i][j]) {
                        mx[i][j] = cand[t]
                    }
                    if (cand[t] < mn[i][j]) {
                        mn[i][j] = cand[t]
                    }
                }
            }
        }
    }
    return mx[0][m - 1]
}
