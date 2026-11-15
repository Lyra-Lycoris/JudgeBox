package t10_max_deletable_edges

func dsuFind(parent: Array<Int64>, x: Int64): Int64 {
    var cur = x
    while (parent[cur] != cur) {
        parent[cur] = parent[parent[cur]]
        cur = parent[cur]
    }
    return cur
}

func dsuUnite(parent: Array<Int64>, size: Array<Int64>, a: Int64, b: Int64): Bool {
    var ra = dsuFind(parent, a)
    var rb = dsuFind(parent, b)
    if (ra == rb) {
        return false
    }
    if (size[ra] < size[rb]) {
        let t = ra
        ra = rb
        rb = t
    }
    parent[rb] = ra
    size[ra] += size[rb]
    return true
}

func solve(n: Int64, m: Int64, e: Array<Array<Int64>>): Int64 {
    let parent = Array<Int64>(n + 1, repeat: 0)
    let size = Array<Int64>(n + 1, repeat: 1)
    for (i in 0..(n + 1)) {
        parent[i] = i
    }
    var components = n
    for (i in 0..m) {
        if (dsuUnite(parent, size, e[i][0], e[i][1])) {
            components -= 1
        }
    }
    return m - (n - components)
}
