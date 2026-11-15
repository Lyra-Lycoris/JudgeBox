package t25_matrix_rowcol_sum

func solve(n: Int64, m: Int64, r: Array<Int64>, c: Array<Int64>): Array<Int64> {
    let row = Array<Int64>(n, repeat: 0)
    let col = Array<Int64>(m, repeat: 0)
    for (i in 0..n) {
        row[i] = r[i]
    }
    for (j in 0..m) {
        col[j] = c[j]
    }
    let a = Array<Int64>(n * m, repeat: 0)
    var at: Int64 = 0
    for (i in 0..n) {
        for (j in 0..m) {
            var x = row[i]
            if (col[j] < x) {
                x = col[j]
            }
            a[at] = x
            at += 1
            row[i] -= x
            col[j] -= x
        }
    }
    return a
}
