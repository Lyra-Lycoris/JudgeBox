package t05_range_add_queries

func solve(n: Int64, a: Array<Int64>, q: Int64, ops: Array<Array<Int64>>): Array<Int64> {
    let diff = Array<Int64>(n + 1, repeat: 0)
    for (j in 0..q) {
        let l = ops[j][0]
        let r = ops[j][1]
        let v = ops[j][2]
        diff[l - 1] = diff[l - 1] + v
        diff[r] = diff[r] - v
    }
    let answer = Array<Int64>(n, repeat: 0)
    var cur: Int64 = 0
    for (i in 0..n) {
        cur = cur + diff[i]
        answer[i] = a[i] + cur
    }
    return answer
}
