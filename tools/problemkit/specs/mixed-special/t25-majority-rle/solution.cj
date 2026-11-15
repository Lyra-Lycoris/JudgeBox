package t25_majority_rle

func solve(k: Int64, v: Array<Int64>, c: Array<Int64>): Int64 {
    var cand: Int64 = 0
    var balance: Int64 = 0
    for (i in 0..k) {
        let cnt = c[i]
        if (balance == 0) {
            cand = v[i]
            balance = cnt
        } else if (v[i] == cand) {
            balance += cnt
        } else if (cnt < balance) {
            balance -= cnt
        } else {
            cand = v[i]
            balance = cnt - balance
        }
    }
    return cand
}
