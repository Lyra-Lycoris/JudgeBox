package t15_path_weight_sum

func solve(n: Int64, w: Array<Int64>, e: Array<Int64>, q: Int64, queries: Array<Int64>): Array<Int64> {
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
    let depth = Array<Int64>(n + 1, repeat: 0)
    let pre = Array<Int64>(n + 1, repeat: 0)
    let visited = Array<Bool>(n + 1, repeat: false)
    let queue = Array<Int64>(n + 1, repeat: 0)
    var qh = 0
    var qt = 0
    queue[qt] = 1
    qt += 1
    visited[1] = true
    pre[1] = w[0]
    while (qh < qt) {
        let u = queue[qh]
        qh += 1
        for (i in head[u]..head[u + 1]) {
            let v = adj[i]
            if (!visited[v]) {
                visited[v] = true
                parent[v] = u
                depth[v] = depth[u] + 1
                pre[v] = pre[u] + w[v - 1]
                queue[qt] = v
                qt += 1
            }
        }
    }

    var log = 1
    while ((1 << log) <= n) {
        log += 1
    }
    let up = Array<Array<Int64>>(log, { _ => Array<Int64>(n + 1, repeat: 1) })
    for (v in 1..(n + 1)) {
        up[0][v] = parent[v]
    }
    for (k in 1..log) {
        for (v in 1..(n + 1)) {
            up[k][v] = up[k - 1][up[k - 1][v]]
        }
    }

    let answer = Array<Int64>(q, repeat: 0)
    for (t in 0..q) {
        let u = queries[2 * t]
        let v = queries[2 * t + 1]
        var a = u
        var b = v
        if (depth[a] < depth[b]) {
            let tmp = a
            a = b
            b = tmp
        }
        var diff = depth[a] - depth[b]
        var k = 0
        while (diff > 0) {
            if (diff % 2 == 1) {
                a = up[k][a]
            }
            diff /= 2
            k += 1
        }
        if (a != b) {
            var bit = log - 1
            while (bit >= 0) {
                if (up[bit][a] != up[bit][b]) {
                    a = up[bit][a]
                    b = up[bit][b]
                }
                bit -= 1
            }
            a = up[0][a]
        }
        answer[t] = pre[u] + pre[v] - 2 * pre[a] + w[a - 1]
    }
    return answer
}
