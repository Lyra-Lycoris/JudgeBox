package t10_relative_queries

func dsuFind(parent: Array<Int64>, x: Int64): Int64 {
    var cur = x
    while (parent[cur] != cur) {
        parent[cur] = parent[parent[cur]]
        cur = parent[cur]
    }
    return cur
}

func dsuUnion(parent: Array<Int64>, size: Array<Int64>, a: Int64, b: Int64): Unit {
    var ra = dsuFind(parent, a)
    var rb = dsuFind(parent, b)
    if (ra != rb) {
        if (size[ra] < size[rb]) {
            let t = ra
            ra = rb
            rb = t
        }
        parent[rb] = ra
        size[ra] += size[rb]
    }
}

func solve(n: Int64, k: Int64, rel: Array<Array<Int64>>, q: Int64, qs: Array<Array<Int64>>): Int64 {
    let parent = Array<Int64>(n + 1, repeat: 0)
    let size = Array<Int64>(n + 1, repeat: 1)
    for (i in 0..(n + 1)) {
        parent[i] = i
    }
    for (i in 0..k) {
        dsuUnion(parent, size, rel[i][0], rel[i][1])
    }
    var answer: Int64 = 0
    for (i in 0..q) {
        if (dsuFind(parent, qs[i][0]) == dsuFind(parent, qs[i][1])) {
            answer += 1
        }
    }
    return answer
}
