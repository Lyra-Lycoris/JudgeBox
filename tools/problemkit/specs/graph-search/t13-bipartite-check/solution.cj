package t13_bipartite_check

func solve(n: Int64, m: Int64, e: Array<Array<Int64>>): Bool {
    let size = n + 2
    let deg = Array<Int64>(size, repeat: 0)
    let start = Array<Int64>(size, repeat: 0)
    for (i in 0..m) {
        let a = e[i][0]
        let b = e[i][1]
        deg[a] += 1
        deg[b] += 1
    }
    let np1 = n + 1
    var acc: Int64 = 0
    for (v in 1..np1) {
        start[v] = acc
        acc += deg[v]
    }
    start[n + 1] = acc
    let cursor = start.clone()
    let adj = Array<Int64>(2 * m, repeat: 0)
    for (i in 0..m) {
        let a = e[i][0]
        let b = e[i][1]
        adj[cursor[a]] = b
        cursor[a] += 1
        adj[cursor[b]] = a
        cursor[b] += 1
    }
    let color = Array<Int64>(size, repeat: -1)
    let queue = Array<Int64>(n, repeat: 0)
    for (s in 1..np1) {
        if (color[s] != -1) {
            continue
        }
        color[s] = 0
        var head: Int64 = 0
        var tail: Int64 = 0
        queue[tail] = s
        tail += 1
        while (head < tail) {
            let u = queue[head]
            head += 1
            let c = color[u] ^ 1
            var k = start[u]
            while (k < start[u + 1]) {
                let v = adj[k]
                if (color[v] == -1) {
                    color[v] = c
                    queue[tail] = v
                    tail += 1
                } else if (color[v] == color[u]) {
                    return false
                }
                k += 1
            }
        }
    }
    return true
}
