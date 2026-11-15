package t15_tree_diameter

func bfsFarthest(head: Array<Int64>, adj: Array<Int64>, n: Int64, src: Int64, dist: Array<Int64>): Int64 {
    for (i in 0..(n + 1)) {
        dist[i] = -1
    }
    let queue = Array<Int64>(n + 1, repeat: 0)
    var qh = 0
    var qt = 0
    queue[qt] = src
    qt += 1
    dist[src] = 0
    while (qh < qt) {
        let u = queue[qh]
        qh += 1
        for (i in head[u]..head[u + 1]) {
            let v = adj[i]
            if (dist[v] < 0) {
                dist[v] = dist[u] + 1
                queue[qt] = v
                qt += 1
            }
        }
    }
    var far = src
    for (i in 1..(n + 1)) {
        if (dist[i] > dist[far]) {
            far = i
        }
    }
    return far
}

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
    let dist = Array<Int64>(n + 1, repeat: -1)
    let a = bfsFarthest(head, adj, n, 1, dist)
    let b = bfsFarthest(head, adj, n, a, dist)
    return dist[b]
}
