package t10_score_consistency

func diffFind(parent: Array<Int64>, diff: Array<Int64>, x: Int64): Int64 {
    var root = x
    var total: Int64 = 0
    while (parent[root] != root) {
        total += diff[root]
        root = parent[root]
    }
    var cur = x
    var remain = total
    while (parent[cur] != cur) {
        let nxt = parent[cur]
        let old = diff[cur]
        parent[cur] = root
        diff[cur] = remain
        remain -= old
        cur = nxt
    }
    return root
}

func solve(n: Int64, k: Int64, rel: Array<Array<Int64>>): Bool {
    let parent = Array<Int64>(n + 1, repeat: 0)
    let size = Array<Int64>(n + 1, repeat: 1)
    let diff = Array<Int64>(n + 1, repeat: 0)
    for (i in 0..(n + 1)) {
        parent[i] = i
    }
    for (i in 0..k) {
        let a = rel[i][0]
        let b = rel[i][1]
        let c = rel[i][2]
        var ra = diffFind(parent, diff, a)
        let da = diff[a]
        var rb = diffFind(parent, diff, b)
        let db = diff[b]
        if (ra == rb) {
            if (da - db != c) {
                return false
            }
            continue
        }
        if (size[ra] < size[rb]) {
            parent[ra] = rb
            diff[ra] = -(da - db - c)
            size[rb] += size[ra]
        } else {
            parent[rb] = ra
            diff[rb] = da - db - c
            size[ra] += size[rb]
        }
    }
    return true
}
