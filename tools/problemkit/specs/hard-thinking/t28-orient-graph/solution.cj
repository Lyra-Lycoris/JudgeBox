package t28_orient_graph

import std.collection.*

func orientFind(dsu: Array<Int64>, x0: Int64): Int64 {
    var x = x0
    while (dsu[x] != x) {
        dsu[x] = dsu[dsu[x]]
        x = dsu[x]
    }
    return x
}

func solve(n: Int64, m: Int64, e: Array<Array<Int64>>): Array<Int64> {
    let dsu = Array<Int64>(n + 1, repeat: 0)
    let dsuSize = Array<Int64>(n + 1, repeat: 1)
    for (i in 0..(n + 1)) {
        dsu[i] = i
    }
    for (i in 0..m) {
        var a = orientFind(dsu, e[i][0])
        var b = orientFind(dsu, e[i][1])
        if (a == b) {
            continue
        }
        if (dsuSize[a] < dsuSize[b]) {
            let t = a
            a = b
            b = t
        }
        dsu[b] = a
        dsuSize[a] += dsuSize[b]
    }

    let edgeCnt = Array<Int64>(n + 1, repeat: 0)
    for (i in 0..m) {
        let r = orientFind(dsu, e[i][0])
        edgeCnt[r] += 1
    }
    for (v in 1..(n + 1)) {
        if (dsu[v] == v && edgeCnt[v] > dsuSize[v]) {
            return [-1]
        }
    }

    let head = Array<Int64>(n + 1, repeat: -1)
    let to = Array<Int64>(2 * m, repeat: 0)
    let nxt = Array<Int64>(2 * m, repeat: 0)
    let eid = Array<Int64>(2 * m, repeat: 0)
    var cnt: Int64 = 0
    for (i in 0..m) {
        let a = e[i][0]
        let b = e[i][1]
        to[cnt] = b
        eid[cnt] = i
        nxt[cnt] = head[a]
        head[a] = cnt
        cnt += 1
        to[cnt] = a
        eid[cnt] = i
        nxt[cnt] = head[b]
        head[b] = cnt
        cnt += 1
    }

    let visited = Array<Bool>(n + 1, repeat: false)
    let parent = Array<Int64>(n + 1, repeat: 0)
    let depth = Array<Int64>(n + 1, repeat: 0)
    let pedge = Array<Int64>(n + 1, repeat: -1)
    let cur = head.clone()
    let answer = Array<Int64>(2 * m, repeat: 0)
    let stack = ArrayList<Int64>()
    for (s in 1..(n + 1)) {
        if (visited[s]) {
            continue
        }
        visited[s] = true
        parent[s] = 0
        depth[s] = 0
        stack.add(s)
        while (stack.size > 0) {
            let u = stack[stack.size - 1]
            let j = cur[u]
            if (j == -1) {
                stack.remove(at: stack.size - 1)
                continue
            }
            cur[u] = nxt[j]
            let v = to[j]
            let k = eid[j]
            if (k == pedge[u]) {
                continue
            }
            if (!visited[v]) {
                visited[v] = true
                parent[v] = u
                pedge[v] = k
                depth[v] = depth[u] + 1
                answer[2 * k] = u
                answer[2 * k + 1] = v
                stack.add(v)
            } else if (depth[v] < depth[u]) {
                answer[2 * k] = u
                answer[2 * k + 1] = v
                var c = v
                while (parent[c] != 0) {
                    let k2 = pedge[c]
                    answer[2 * k2] = c
                    answer[2 * k2 + 1] = parent[c]
                    c = parent[c]
                }
            }
        }
    }
    return answer
}
