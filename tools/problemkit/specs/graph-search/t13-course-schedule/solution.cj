package t13_course_schedule

func solve(n: Int64, m: Int64, e: Array<Array<Int64>>): Bool {
    let size = n + 2
    let deg = Array<Int64>(size, repeat: 0)
    let indeg = Array<Int64>(size, repeat: 0)
    let start = Array<Int64>(size, repeat: 0)
    for (i in 0..m) {
        let a = e[i][0]
        let b = e[i][1]
        deg[a] += 1
        indeg[b] += 1
    }
    let np1 = n + 1
    var acc: Int64 = 0
    for (v in 1..np1) {
        start[v] = acc
        acc += deg[v]
    }
    start[n + 1] = acc
    let cursor = start.clone()
    let adj = Array<Int64>(m, repeat: 0)
    for (i in 0..m) {
        let a = e[i][0]
        let b = e[i][1]
        adj[cursor[a]] = b
        cursor[a] += 1
    }
    let queue = Array<Int64>(n, repeat: 0)
    var head: Int64 = 0
    var tail: Int64 = 0
    for (v in 1..np1) {
        if (indeg[v] == 0) {
            queue[tail] = v
            tail += 1
        }
    }
    var seen: Int64 = 0
    while (head < tail) {
        let u = queue[head]
        head += 1
        seen += 1
        var k = start[u]
        while (k < start[u + 1]) {
            let b = adj[k]
            indeg[b] -= 1
            if (indeg[b] == 0) {
                queue[tail] = b
                tail += 1
            }
            k += 1
        }
    }
    return seen == n
}
