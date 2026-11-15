package t14_kruskal_mst

import std.sort.*

func solve(n: Int64, m: Int64, e: Array<Array<Int64>>): Int64 {
    let OFF: Int64 = 1000000000
    let base = m + 1
    let keys = Array<Int64>(m, repeat: 0)
    var i: Int64 = 0
    while (i < m) {
        keys[i] = (e[i][2] + OFF) * base + i
        i += 1
    }
    sort(keys)
    let parent = Array<Int64>(n + 1, repeat: 0)
    var v: Int64 = 0
    while (v <= n) {
        parent[v] = v
        v += 1
    }
    var total: Int64 = 0
    var used: Int64 = 0
    var k: Int64 = 0
    while (k < m && used < n - 1) {
        let idx = keys[k] % base
        let w = keys[k] / base - OFF
        var ru = e[idx][0]
        while (parent[ru] != ru) {
            parent[ru] = parent[parent[ru]]
            ru = parent[ru]
        }
        var rv = e[idx][1]
        while (parent[rv] != rv) {
            parent[rv] = parent[parent[rv]]
            rv = parent[rv]
        }
        if (ru != rv) {
            parent[ru] = rv
            total += w
            used += 1
        }
        k += 1
    }
    return total
}
