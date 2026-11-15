package t17_course_tree_knapsack

import std.collection.*

func dfsCourse(u: Int64, children: Array<ArrayList<Int64>>, profit: Array<Int64>,
    limit: Int64): Array<Int64> {
    var f = Array<Int64>(2, repeat: 0)
    f[0] = 0
    if (u == 0) {
        f[1] = 0
    } else {
        f[1] = profit[u - 1]
    }
    var size = 1
    for (ch in children[u]) {
        let fc = dfsCourse(ch, children, profit, limit)
        let sc = fc.size - 1
        var newcap = size + sc
        if (newcap > limit) {
            newcap = limit
        }
        let g = Array<Int64>(newcap + 1, repeat: -4000000000000000000)
        g[0] = 0
        var j = 1
        while (j <= size) {
            var t = 0
            while (t <= sc && j + t <= newcap) {
                let val = f[j] + fc[t]
                if (val > g[j + t]) {
                    g[j + t] = val
                }
                t += 1
            }
            j += 1
        }
        f = g
        size = newcap
    }
    return f
}

func solve(n: Int64, k: Int64, parent: Array<Int64>, profit: Array<Int64>): Int64 {
    let children = Array<ArrayList<Int64>>(n + 1, { _ => ArrayList<Int64>() })
    for (i in 1..n + 1) {
        children[parent[i - 1]].add(i)
    }
    let f = dfsCourse(0, children, profit, k + 1)
    return f[k + 1]
}
