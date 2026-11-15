package t05_submatrix_queries

func solve(n: Int64, m: Int64, g: Array<Array<Int64>>, q: Int64, queries: Array<Array<Int64>>): Array<Int64> {
    let pre = Array<Array<Int64>>(n + 1, { _ => Array<Int64>(m + 1, repeat: 0) })
    for (i in 1..n + 1) {
        var running: Int64 = 0
        for (j in 1..m + 1) {
            running = running + g[i - 1][j - 1]
            pre[i][j] = pre[i - 1][j] + running
        }
    }
    let answer = Array<Int64>(q, repeat: 0)
    for (t in 0..q) {
        let x1 = queries[t][0]
        let y1 = queries[t][1]
        let x2 = queries[t][2]
        let y2 = queries[t][3]
        answer[t] = pre[x2][y2] - pre[x1 - 1][y2] - pre[x2][y1 - 1] + pre[x1 - 1][y1 - 1]
    }
    return answer
}
