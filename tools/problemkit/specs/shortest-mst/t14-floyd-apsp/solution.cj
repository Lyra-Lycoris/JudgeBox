package t14_floyd_apsp

func solve(n: Int64, w: Array<Array<Int64>>): Array<Int64> {
    let INF: Int64 = 1 << 62
    let d = Array<Array<Int64>>(n, { _ => Array<Int64>(n, repeat: INF) })
    var i: Int64 = 0
    while (i < n) {
        var j: Int64 = 0
        while (j < n) {
            if (w[i][j] >= 0) {
                d[i][j] = w[i][j]
            }
            j += 1
        }
        d[i][i] = 0
        i += 1
    }
    var k: Int64 = 0
    while (k < n) {
        i = 0
        while (i < n) {
            let dik = d[i][k]
            if (dik < INF) {
                var j: Int64 = 0
                while (j < n) {
                    let nd = dik + d[k][j]
                    if (nd < d[i][j]) {
                        d[i][j] = nd
                    }
                    j += 1
                }
            }
            i += 1
        }
        k += 1
    }
    let answer = Array<Int64>(n * n, repeat: 0)
    i = 0
    while (i < n) {
        var j: Int64 = 0
        while (j < n) {
            let x = d[i][j]
            if (x >= INF) {
                answer[i * n + j] = -1
            } else {
                answer[i * n + j] = x
            }
            j += 1
        }
        i += 1
    }
    return answer
}
