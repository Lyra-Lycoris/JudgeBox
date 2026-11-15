package t13_graph_components

func solve(n: Int64, m: Int64, e: Array<Array<Int64>>): Int64 {
    let total = n + 1
    let parent = Array<Int64>(total, repeat: 0)
    let rnk = Array<Int64>(total, repeat: 0)
    for (i in 0..total) {
        parent[i] = i
    }
    var count = n
    for (i in 0..m) {
        var a = e[i][0]
        var b = e[i][1]
        while (parent[a] != a) {
            parent[a] = parent[parent[a]]
            a = parent[a]
        }
        while (parent[b] != b) {
            parent[b] = parent[parent[b]]
            b = parent[b]
        }
        if (a == b) {
            continue
        }
        if (rnk[a] < rnk[b]) {
            let t = a
            a = b
            b = t
        }
        parent[b] = a
        if (rnk[a] == rnk[b]) {
            rnk[a] += 1
        }
        count -= 1
    }
    return count
}
