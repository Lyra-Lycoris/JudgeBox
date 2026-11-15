package t15_sum_pair_dist

func solve(n: Int64, e: Array<Int64>): Int64 {
    if (n <= 1) {
        return 0
    }
    let m = e.size / 2
    let deg = Array<Int64>(n + 2, repeat: 0)
    for (i in 0..m) {
        deg[e[2 * i]] += 1
        deg[e[2 * i + 1]] += 1
    }
    let head = Array<Int64>(n + 2, repeat: 0)
    for (i in 1..(n + 1)) {
        head[i + 1] = head[i] + deg[i]
    }
    let adj = Array<Int64>(2 * m, repeat: 0)
    let pos = head.clone()
    for (i in 0..m) {
        let u = e[2 * i]
        let v = e[2 * i + 1]
        adj[pos[u]] = v
        pos[u] += 1
        adj[pos[v]] = u
        pos[v] += 1
    }

    let parent = Array<Int64>(n + 1, repeat: 1)
    let order = Array<Int64>(n, repeat: 0)
    let visited = Array<Bool>(n + 1, repeat: false)
    var cnt = 0
    order[cnt] = 1
    cnt += 1
    visited[1] = true
    var i = 0
    while (i < cnt) {
        let u = order[i]
        i += 1
        for (j in head[u]..head[u + 1]) {
            let v = adj[j]
            if (!visited[v]) {
                visited[v] = true
                parent[v] = u
                order[cnt] = v
                cnt += 1
            }
        }
    }

    let size = Array<Int64>(n + 1, repeat: 1)
    var total = 0
    var k = n - 1
    while (k > 0) {
        let v = order[k]
        let s = size[v]
        total += s * (n - s)
        size[parent[v]] += s
        k -= 1
    }
    return total
}
