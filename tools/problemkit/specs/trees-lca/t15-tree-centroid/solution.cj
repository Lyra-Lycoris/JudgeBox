package t15_tree_centroid

func solve(n: Int64, e: Array<Int64>): Int64 {
    if (n == 1) {
        return 1
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
    var k = n - 1
    while (k > 0) {
        let v = order[k]
        size[parent[v]] += size[v]
        k -= 1
    }
    let maxPart = Array<Int64>(n + 1, repeat: 0)
    for (v in 1..(n + 1)) {
        maxPart[v] = n - size[v]
    }
    var t = 1
    while (t < n) {
        let v = order[t]
        let p = parent[v]
        if (size[v] > maxPart[p]) {
            maxPart[p] = size[v]
        }
        t += 1
    }
    var best = 1
    var found = false
    for (v in 1..(n + 1)) {
        if (!found && maxPart[v] * 2 <= n) {
            best = v
            found = true
        }
    }
    return best
}
