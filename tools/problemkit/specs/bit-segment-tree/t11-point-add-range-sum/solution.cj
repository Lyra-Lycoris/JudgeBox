package t11_point_add_range_sum

func solve(n: Int64, a: Array<Int64>, q: Int64, ops: Array<Array<Int64>>): Array<Int64> {
    let tree = Array<Int64>(n + 1, repeat: 0)
    for (i in 1..n + 1) {
        tree[i] = tree[i] + a[i - 1]
        let up = i + (i & -i)
        if (up <= n) {
            tree[up] = tree[up] + tree[i]
        }
    }
    var count: Int64 = 0
    for (j in 0..q) {
        if (ops[j][0] == 2) {
            count += 1
        }
    }
    let answer = Array<Int64>(count, repeat: 0)
    var at: Int64 = 0
    for (j in 0..q) {
        if (ops[j][0] == 1) {
            var i = ops[j][1]
            let v = ops[j][2]
            while (i <= n) {
                tree[i] = tree[i] + v
                i = i + (i & -i)
            }
        } else {
            var sum: Int64 = 0
            var i = ops[j][2]
            while (i > 0) {
                sum = sum + tree[i]
                i = i - (i & -i)
            }
            i = ops[j][1] - 1
            while (i > 0) {
                sum = sum - tree[i]
                i = i - (i & -i)
            }
            answer[at] = sum
            at += 1
        }
    }
    return answer
}
