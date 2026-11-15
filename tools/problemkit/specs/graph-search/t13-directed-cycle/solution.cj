package t13_directed_cycle

import std.collection.*

func solve(n: Int64, m: Int64, e: Array<Array<Int64>>): Int64 {
    let size = n + 2
    let deg = Array<Int64>(size, repeat: 0)
    let indeg = Array<Int64>(size, repeat: 0)
    let start = Array<Int64>(size, repeat: 0)
    let rstart = Array<Int64>(size, repeat: 0)
    let hasSelf = Array<Int64>(size, repeat: 0)
    for (i in 0..m) {
        let a = e[i][0]
        let b = e[i][1]
        deg[a] += 1
        indeg[b] += 1
        if (a == b) {
            hasSelf[a] = 1
        }
    }
    let np1 = n + 1
    for (v in 1..np1) {
        start[v + 1] = start[v] + deg[v]
        rstart[v + 1] = rstart[v] + indeg[v]
    }
    let cursor = start.clone()
    let rcursor = rstart.clone()
    let adj = Array<Int64>(m, repeat: 0)
    let radj = Array<Int64>(m, repeat: 0)
    for (i in 0..m) {
        let a = e[i][0]
        let b = e[i][1]
        adj[cursor[a]] = b
        cursor[a] += 1
        radj[rcursor[b]] = a
        rcursor[b] += 1
    }
    let visited = Array<Int64>(size, repeat: 0)
    let order = Array<Int64>(n, repeat: 0)
    let stackArr = Array<Int64>(n, repeat: 0)
    let it = start.clone()
    var on: Int64 = 0
    for (s in 1..np1) {
        if (visited[s] != 0) {
            continue
        }
        visited[s] = 1
        var sp: Int64 = 1
        stackArr[0] = s
        while (sp > 0) {
            let u = stackArr[sp - 1]
            if (it[u] < start[u + 1]) {
                let v = adj[it[u]]
                it[u] += 1
                if (visited[v] == 0) {
                    visited[v] = 1
                    stackArr[sp] = v
                    sp += 1
                }
            } else {
                order[on] = u
                on += 1
                sp -= 1
            }
        }
    }
    let comp = Array<Int64>(size, repeat: -1)
    let sizes = ArrayList<Int64>()
    var idx = n - 1
    while (idx >= 0) {
        let s = order[idx]
        if (comp[s] == -1) {
            let cid = sizes.size
            comp[s] = cid
            var count: Int64 = 0
            var sp: Int64 = 1
            stackArr[0] = s
            while (sp > 0) {
                sp -= 1
                let u = stackArr[sp]
                count += 1
                var k = rstart[u]
                while (k < rstart[u + 1]) {
                    let v = radj[k]
                    if (comp[v] == -1) {
                        comp[v] = cid
                        stackArr[sp] = v
                        sp += 1
                    }
                    k += 1
                }
            }
            sizes.add(count)
        }
        idx -= 1
    }
    var answer: Int64 = 0
    for (csize in sizes) {
        if (csize > 1) {
            answer += csize
        }
    }
    for (v in 1..np1) {
        if (hasSelf[v] == 1 && sizes[comp[v]] == 1) {
            answer += 1
        }
    }
    return answer
}
