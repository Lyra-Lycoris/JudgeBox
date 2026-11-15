package t10_cycle_detect

func dsuFind(parent: Array<Int64>, x: Int64): Int64 {
    var cur = x
    while (parent[cur] != cur) {
        parent[cur] = parent[parent[cur]]
        cur = parent[cur]
    }
    return cur
}

func solve(n: Int64, m: Int64, e: Array<Array<Int64>>): Bool {
    let parent = Array<Int64>(n + 1, repeat: 0)
    let size = Array<Int64>(n + 1, repeat: 1)
    for (i in 0..(n + 1)) {
        parent[i] = i
    }
    for (i in 0..m) {
        var a = dsuFind(parent, e[i][0])
        var b = dsuFind(parent, e[i][1])
        if (a == b) {
            return true
        }
        if (size[a] < size[b]) {
            let t = a
            a = b
            b = t
        }
        parent[b] = a
        size[a] += size[b]
    }
    return false
}
