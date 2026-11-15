package t11_range_add_point_get

func solve(n: Int64, a: Array<Int64>, q: Int64, ops: Array<Array<Int64>>): Array<Int64> {
    let tree = Array<Int64>(n + 2, repeat: 0)
    var count: Int64 = 0
    for (j in 0..q) {
        if (ops[j][0] == 2) {
            count += 1
        }
    }
    let answer = Array<Int64>(count, repeat: 0)
    var at: Int64 = 0
    for (j in 0..q) {
        let t = ops[j][0]
        let l = ops[j][1]
        let r = ops[j][2]
        let v = ops[j][3]
        if (t == 1) {
            var i = l
            while (i <= n) {
                tree[i] = tree[i] + v
                i = i + (i & -i)
            }
            i = r + 1
            while (i <= n) {
                tree[i] = tree[i] - v
                i = i + (i & -i)
            }
        } else {
            var sum: Int64 = 0
            var i = l
            while (i > 0) {
                sum = sum + tree[i]
                i = i - (i & -i)
            }
            answer[at] = a[l - 1] + sum
            at += 1
        }
    }
    return answer
}
