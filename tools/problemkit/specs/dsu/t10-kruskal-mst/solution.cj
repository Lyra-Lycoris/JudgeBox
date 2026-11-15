package t10_kruskal_mst

import std.sort.*

struct Edge {
    Edge(let u: Int64, let v: Int64, let w: Int64) {}
}

func edgeLess(a: Edge, b: Edge): Ordering {
    if (a.w < b.w) {
        return Ordering.LT
    }
    if (a.w > b.w) {
        return Ordering.GT
    }
    return Ordering.EQ
}

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
    let edges = Array<Edge>(m) { i => Edge(e[i][0], e[i][1], e[i][2]) }
    sort(edges, by: edgeLess)
    let parent = Array<Int64>(n + 1, repeat: 0)
    let size = Array<Int64>(n + 1, repeat: 1)
    for (i in 0..(n + 1)) {
        parent[i] = i
    }
    var total: Int64 = 0
    var used: Int64 = 0
    for (i in 0..m) {
        if (dsuUnite(parent, size, edges[i].u, edges[i].v)) {
            total += edges[i].w
            used += 1
        }
    }
    if (used != n - 1) {
        return -1
    }
    return total
}
