package t02_max_sum_submatrix

func solve(n: Int64, m: Int64, g: Array<Array<Int64>>): Int64 {
    var answer = g[0][0]
    let sums = Array<Int64>(m, repeat: 0)
    var top: Int64 = 0
    while (top < n) {
        for (c in 0..m) {
            sums[c] = 0
        }
        var bottom = top
        while (bottom < n) {
            for (c in 0..m) {
                sums[c] += g[bottom][c]
            }
            var cur = sums[0]
            var best = sums[0]
            var c: Int64 = 1
            while (c < m) {
                if (cur < 0) {
                    cur = sums[c]
                } else {
                    cur = cur + sums[c]
                }
                if (cur > best) {
                    best = cur
                }
                c += 1
            }
            if (best > answer) {
                answer = best
            }
            bottom += 1
        }
        top += 1
    }
    return answer
}
