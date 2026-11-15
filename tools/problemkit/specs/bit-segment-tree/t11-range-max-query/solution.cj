package t11_range_max_query

func solve(n: Int64, a: Array<Int64>, q: Int64, queries: Array<Array<Int64>>): Array<Int64> {
    let lg = Array<Int64>(n + 1, repeat: 0)
    for (i in 2..n + 1) {
        lg[i] = lg[i / 2] + 1
    }
    var levels: Int64 = 1
    while ((1 << levels) <= n) {
        levels += 1
    }
    let table = Array<Array<Int64>>(levels, { _ => a.clone() })
    table[0] = a
    for (j in 1..levels) {
        let len = n - (1 << j) + 1
        let half = 1 << (j - 1)
        let prev = table[j - 1]
        for (i in 0..len) {
            let x = prev[i]
            let y = prev[i + half]
            if (x >= y) {
                table[j][i] = x
            } else {
                table[j][i] = y
            }
        }
    }
    let answer = Array<Int64>(q, repeat: 0)
    for (k in 0..q) {
        let l = queries[k][0]
        let r = queries[k][1]
        let level = lg[r - l + 1]
        let x = table[level][l - 1]
        let y = table[level][r - (1 << level)]
        if (x >= y) {
            answer[k] = x
        } else {
            answer[k] = y
        }
    }
    return answer
}
