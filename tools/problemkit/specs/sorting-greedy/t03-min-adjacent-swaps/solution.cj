package t03_min_adjacent_swaps

import std.sort.*

func solve(n: Int64, a: Array<Int64>): Int64 {
    let shift = 1000000000
    let base = 1048576
    let keys = Array<Int64>(n, repeat: 0)
    for (i in 0..n) {
        keys[i] = (a[i] + shift) * base + i
    }
    sort(keys)
    let perm = Array<Int64>(n, repeat: 0)
    for (p in 0..n) {
        perm[keys[p] % base] = p + 1
    }
    let tree = Array<Int64>(n + 1, repeat: 0)
    var total = 0
    for (i in 0..n) {
        let v = perm[i]
        var sum = 0
        var x = v
        while (x > 0) {
            sum += tree[x]
            x -= x & (-x)
        }
        total += i - sum
        x = v
        while (x <= n) {
            tree[x] += 1
            x += x & (-x)
        }
    }
    return total
}
