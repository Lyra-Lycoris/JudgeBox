package t10_island_count

func dsuFind(parent: Array<Int64>, x: Int64): Int64 {
    var cur = x
    while (parent[cur] != cur) {
        parent[cur] = parent[parent[cur]]
        cur = parent[cur]
    }
    return cur
}

func dsuUnion(parent: Array<Int64>, size: Array<Int64>, a: Int64, b: Int64): Bool {
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

func solve(n: Int64, m: Int64, g: Array<Array<Int64>>): Int64 {
    let total = n * m
    let parent = Array<Int64>(total, repeat: 0)
    let size = Array<Int64>(total, repeat: 1)
    for (i in 0..total) {
        parent[i] = i
    }
    var islands: Int64 = 0
    for (r in 0..n) {
        for (c in 0..m) {
            if (g[r][c] != 1) {
                continue
            }
            islands += 1
            let cur = r * m + c
            if (r > 0 && g[r - 1][c] == 1) {
                if (dsuUnion(parent, size, cur, cur - m)) {
                    islands -= 1
                }
            }
            if (c > 0 && g[r][c - 1] == 1) {
                if (dsuUnion(parent, size, cur, cur - 1)) {
                    islands -= 1
                }
            }
        }
    }
    return islands
}
