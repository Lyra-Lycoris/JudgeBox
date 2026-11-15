package t14_bottleneck_queries

import std.collection.*
import std.sort.*

func solve(n: Int64, m: Int64, q: Int64, e: Array<Array<Int64>>, queries: Array<Array<Int64>>): Array<Int64> {
    let base = m + 1
    let keys = Array<Int64>(m, repeat: 0)
    var i: Int64 = 0
    while (i < m) {
        keys[i] = e[i][2] * base + i
        i += 1
    }
    sort(keys)
    let parent = Array<Int64>(n + 1, repeat: 0)
    var v: Int64 = 0
    while (v <= n) {
        parent[v] = v
        v += 1
    }
    let head = Array<Int64>(n + 1, repeat: -1)
    let to = Array<Int64>(2 * (n - 1), repeat: 0)
    let nxt = Array<Int64>(2 * (n - 1), repeat: -1)
    let wt = Array<Int64>(2 * (n - 1), repeat: 0)
    var cnt: Int64 = 0
    var used: Int64 = 0
    var k: Int64 = 0
    while (k < m && used < n - 1) {
        let idx = keys[k] % base
        let w = keys[k] / base
        let u = e[idx][0]
        let uu = e[idx][1]
        var ru = u
        while (parent[ru] != ru) {
            parent[ru] = parent[parent[ru]]
            ru = parent[ru]
        }
        var rv = uu
        while (parent[rv] != rv) {
            parent[rv] = parent[parent[rv]]
            rv = parent[rv]
        }
        if (ru != rv) {
            parent[ru] = rv
            to[cnt] = uu
            wt[cnt] = w
            nxt[cnt] = head[u]
            head[u] = cnt
            cnt += 1
            to[cnt] = u
            wt[cnt] = w
            nxt[cnt] = head[uu]
            head[uu] = cnt
            cnt += 1
            used += 1
        }
        k += 1
    }
    var LOG: Int64 = 1
    while ((1 << LOG) <= n) {
        LOG += 1
    }
    let up = Array<Array<Int64>>(LOG, { _ => Array<Int64>(n + 1, repeat: 0) })
    let mx = Array<Array<Int64>>(LOG, { _ => Array<Int64>(n + 1, repeat: 0) })
    let depth = Array<Int64>(n + 1, repeat: 0)
    let seen = Array<Bool>(n + 1, repeat: false)
    let stack = ArrayList<Int64>()
    seen[1] = true
    stack.add(1)
    while (stack.size > 0) {
        let u = stack[stack.size - 1]
        stack.remove(at: stack.size - 1)
        var j = head[u]
        while (j != -1) {
            let x = to[j]
            if (!seen[x]) {
                seen[x] = true
                depth[x] = depth[u] + 1
                up[0][x] = u
                mx[0][x] = wt[j]
                stack.add(x)
            }
            j = nxt[j]
        }
    }
    var kk: Int64 = 1
    while (kk < LOG) {
        var node: Int64 = 1
        while (node <= n) {
            let mid = up[kk - 1][node]
            up[kk][node] = up[kk - 1][mid]
            let a = mx[kk - 1][node]
            let b = mx[kk - 1][mid]
            if (a > b) {
                mx[kk][node] = a
            } else {
                mx[kk][node] = b
            }
            node += 1
        }
        kk += 1
    }
    let answer = Array<Int64>(q, repeat: 0)
    var t: Int64 = 0
    while (t < q) {
        var u = queries[t][0]
        var z = queries[t][1]
        var best: Int64 = 0
        if (depth[u] < depth[z]) {
            let tmp = u
            u = z
            z = tmp
        }
        var diff = depth[u] - depth[z]
        var level: Int64 = 0
        while (diff > 0) {
            if (diff % 2 == 1) {
                if (mx[level][u] > best) {
                    best = mx[level][u]
                }
                u = up[level][u]
            }
            diff = diff / 2
            level += 1
        }
        if (u != z) {
            var down = LOG - 1
            while (down >= 0) {
                if (up[down][u] != up[down][z]) {
                    if (mx[down][u] > best) {
                        best = mx[down][u]
                    }
                    if (mx[down][z] > best) {
                        best = mx[down][z]
                    }
                    u = up[down][u]
                    z = up[down][z]
                }
                down -= 1
            }
            if (mx[0][u] > best) {
                best = mx[0][u]
            }
            if (mx[0][z] > best) {
                best = mx[0][z]
            }
        }
        answer[t] = best
        t += 1
    }
    return answer
}
