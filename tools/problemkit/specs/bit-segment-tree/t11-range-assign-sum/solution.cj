package t11_range_assign_sum

let NONE: Int64 = 4611686018427387904
var gSum: Array<Int64> = Array<Int64>(0, repeat: 0)
var gTag: Array<Int64> = Array<Int64>(0, repeat: 0)

func build(node: Int64, l: Int64, r: Int64, a: Array<Int64>): Unit {
    gTag[node] = NONE
    if (l == r) {
        gSum[node] = a[l - 1]
        return
    }
    let mid = (l + r) / 2
    build(node * 2, l, mid, a)
    build(node * 2 + 1, mid + 1, r, a)
    gSum[node] = gSum[node * 2] + gSum[node * 2 + 1]
}

func applyNode(node: Int64, l: Int64, r: Int64, v: Int64): Unit {
    gSum[node] = v * (r - l + 1)
    gTag[node] = v
}

func pushDown(node: Int64, l: Int64, r: Int64): Unit {
    if (gTag[node] == NONE || l == r) {
        return
    }
    let mid = (l + r) / 2
    applyNode(node * 2, l, mid, gTag[node])
    applyNode(node * 2 + 1, mid + 1, r, gTag[node])
    gTag[node] = NONE
}

func update(node: Int64, l: Int64, r: Int64, ql: Int64, qr: Int64, v: Int64): Unit {
    if (ql <= l && r <= qr) {
        applyNode(node, l, r, v)
        return
    }
    pushDown(node, l, r)
    let mid = (l + r) / 2
    if (ql <= mid) {
        update(node * 2, l, mid, ql, qr, v)
    }
    if (qr > mid) {
        update(node * 2 + 1, mid + 1, r, ql, qr, v)
    }
    gSum[node] = gSum[node * 2] + gSum[node * 2 + 1]
}

func solve(n: Int64, a: Array<Int64>, q: Int64, ops: Array<Array<Int64>>): Array<Int64> {
    gSum = Array<Int64>(4 * n + 4, repeat: 0)
    gTag = Array<Int64>(4 * n + 4, repeat: 0)
    build(1, 1, n, a)
    let answer = Array<Int64>(q, repeat: 0)
    for (j in 0..q) {
        update(1, 1, n, ops[j][0], ops[j][1], ops[j][2])
        answer[j] = gSum[1]
    }
    return answer
}
