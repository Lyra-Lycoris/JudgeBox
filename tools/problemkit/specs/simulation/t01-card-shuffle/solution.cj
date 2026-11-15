package t01_card_shuffle

import std.collection.*

func solve(n: Int64, k: Int64, p: Array<Int64>): Array<Int64> {
    let perm = Array<Int64>(n, repeat: 0)
    for (i in 0..n) {
        perm[i] = p[i] - 1
    }
    let answer = Array<Int64>(n, repeat: 0)
    let visited = Array<Bool>(n, repeat: false)
    for (start in 0..n) {
        if (visited[start]) {
            continue
        }
        let cycle = ArrayList<Int64>()
        var current = start
        while (!visited[current]) {
            visited[current] = true
            cycle.add(current)
            current = perm[current]
        }
        let length = cycle.size
        let shift = k % length
        for (j in 0..length) {
            let source = ((j - shift) % length + length) % length
            answer[cycle[j]] = cycle[source] + 1
        }
    }
    return answer
}
