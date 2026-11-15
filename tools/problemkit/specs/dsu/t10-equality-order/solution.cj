package t10_equality_order

func dsuFind(parent: Array<Int64>, x: Int64): Int64 {
    var cur = x
    while (parent[cur] != cur) {
        parent[cur] = parent[parent[cur]]
        cur = parent[cur]
    }
    return cur
}

func dsuUnion(parent: Array<Int64>, size: Array<Int64>, a: Int64, b: Int64): Unit {
    var ra = dsuFind(parent, a)
    var rb = dsuFind(parent, b)
    if (ra != rb) {
        if (size[ra] < size[rb]) {
            let t = ra
            ra = rb
            rb = t
        }
        parent[rb] = ra
        size[ra] += size[rb]
    }
}

func solve(n: Int64, k: Int64, cons: Array<Array<Int64>>): Bool {
    let parent = Array<Int64>(n + 1, repeat: 0)
    let size = Array<Int64>(n + 1, repeat: 1)
    for (i in 0..(n + 1)) {
        parent[i] = i
    }
    for (i in 0..k) {
        if (cons[i][0] == 0) {
            dsuUnion(parent, size, cons[i][1], cons[i][2])
        }
    }

    let ids = Array<Int64>(n + 1, repeat: -1)
    var cnt: Int64 = 0
    for (v in 1..(n + 1)) {
        let r = dsuFind(parent, v)
        if (ids[r] < 0) {
            ids[r] = cnt
            cnt += 1
        }
    }

    let outdeg = Array<Int64>(cnt, repeat: 0)
    for (i in 0..k) {
        if (cons[i][0] != 1) {
            continue
        }
        let u = ids[dsuFind(parent, cons[i][1])]
        let v = ids[dsuFind(parent, cons[i][2])]
        if (u == v) {
            return false
        }
        outdeg[u] += 1
    }

    let start = Array<Int64>(cnt + 1, repeat: 0)
    for (i in 0..cnt) {
        start[i + 1] = start[i] + outdeg[i]
    }
    let to = Array<Int64>(start[cnt], repeat: 0)
    let fill = Array<Int64>(cnt, repeat: 0)
    let indeg = Array<Int64>(cnt, repeat: 0)
    for (i in 0..k) {
        if (cons[i][0] != 1) {
            continue
        }
        let u = ids[dsuFind(parent, cons[i][1])]
        let v = ids[dsuFind(parent, cons[i][2])]
        to[start[u] + fill[u]] = v
        fill[u] += 1
        indeg[v] += 1
    }

    let order = Array<Int64>(cnt, repeat: 0)
    var head: Int64 = 0
    var tail: Int64 = 0
    for (i in 0..cnt) {
        if (indeg[i] == 0) {
            order[tail] = i
            tail += 1
        }
    }
    var seen: Int64 = 0
    while (head < tail) {
        let u = order[head]
        head += 1
        seen += 1
        for (j in start[u]..start[u + 1]) {
            let v = to[j]
            indeg[v] -= 1
            if (indeg[v] == 0) {
                order[tail] = v
                tail += 1
            }
        }
    }
    return seen == cnt
}
