package t28_01_matrix_rows_cols

import std.sort.*

func solve(n: Int64, m: Int64, r: Array<Int64>, c: Array<Int64>): Array<Int64> {
    let SHIFT: Int64 = 100000
    let BIG: Int64 = 99999
    let rem = c.clone()
    let result = Array<Int64>(n * m, repeat: 0)
    let rowKeys = Array<Int64>(n, repeat: 0)
    for (i in 0..n) {
        rowKeys[i] = r[i] * SHIFT + (BIG - i)
    }
    sort(rowKeys)
    let colKeys = Array<Int64>(m, repeat: 0)
    var t = n - 1
    while (t >= 0) {
        let key = rowKeys[t]
        let i = BIG - key % SHIFT
        let need = key / SHIFT
        if (need > 0) {
            for (j in 0..m) {
                colKeys[j] = rem[j] * SHIFT + (BIG - j)
            }
            sort(colKeys)
            var p: Int64 = 0
            while (p < need) {
                let ck = colKeys[m - 1 - p]
                let j = BIG - ck % SHIFT
                result[i * m + j] = 1
                rem[j] -= 1
                p += 1
            }
        }
        t -= 1
    }
    return result
}
