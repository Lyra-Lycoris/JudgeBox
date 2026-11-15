package t18_reroot_distance_sum

func solve(n: Int64, p: Array<Int64>): Array<Int64> {
    let sz = Array<Int64>(n + 1, repeat: 1)
    let depth = Array<Int64>(n + 1, repeat: 0)
    let f = Array<Int64>(n + 1, repeat: 0)
    var i: Int64 = n
    while (i >= 2) {
        sz[p[i - 2]] += sz[i]
        i -= 1
    }
    i = 2
    while (i <= n) {
        depth[i] = depth[p[i - 2]] + 1
        f[1] += depth[i]
        i += 1
    }
    i = 2
    while (i <= n) {
        f[i] = f[p[i - 2]] + n - 2 * sz[i]
        i += 1
    }
    let answer = Array<Int64>(n, repeat: 0)
    i = 1
    while (i <= n) {
        answer[i - 1] = f[i]
        i += 1
    }
    return answer
}
