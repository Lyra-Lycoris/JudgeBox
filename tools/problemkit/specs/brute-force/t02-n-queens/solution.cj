package t02_n_queens

func nqDfs(row: Int64, n: Int64, col: Array<Bool>, d1: Array<Bool>, d2: Array<Bool>): Int64 {
    if (row == n) {
        return 1
    }
    var total: Int64 = 0
    for (c in 0..n) {
        let a = row + c
        let b = row - c + n
        if (col[c] || d1[a] || d2[b]) {
            continue
        }
        col[c] = true
        d1[a] = true
        d2[b] = true
        total += nqDfs(row + 1, n, col, d1, d2)
        col[c] = false
        d1[a] = false
        d2[b] = false
    }
    return total
}

func solve(n: Int64): Int64 {
    let col = Array<Bool>(n, repeat: false)
    let d1 = Array<Bool>(2 * n, repeat: false)
    let d2 = Array<Bool>(2 * n, repeat: false)
    return nqDfs(0, n, col, d1, d2)
}
