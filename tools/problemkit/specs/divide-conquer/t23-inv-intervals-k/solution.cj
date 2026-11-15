package t23_inv_intervals_k

import std.sort.*

func lowerBound(values: Array<Int64>, len: Int64, x: Int64): Int64 {
    var lo: Int64 = 0
    var hi = len
    while (lo < hi) {
        let mid = (lo + hi) / 2
        if (values[mid] < x) {
            lo = mid + 1
        } else {
            hi = mid
        }
    }
    return lo
}

func bitAdd(tree: Array<Int64>, size: Int64, pos: Int64, delta: Int64): Unit {
    var i = pos
    while (i <= size) {
        tree[i] += delta
        i += i & -i
    }
}

func bitSum(tree: Array<Int64>, pos: Int64): Int64 {
    var sum: Int64 = 0
    var i = pos
    while (i > 0) {
        sum += tree[i]
        i -= i & -i
    }
    return sum
}

func solve(n: Int64, k: Int64, a: Array<Int64>): Int64 {
    if (k <= 0) {
        return n * (n + 1) / 2
    }
    let values = Array<Int64>(n, repeat: 0)
    for (i in 0..n) {
        values[i] = a[i]
    }
    sort(values)
    var m: Int64 = 0
    for (i in 0..n) {
        if (i == 0 || values[i] != values[i - 1]) {
            values[m] = values[i]
            m += 1
        }
    }
    let tree = Array<Int64>(m + 1, repeat: 0)
    var answer: Int64 = 0
    var windowSize: Int64 = 0
    var inversions: Int64 = 0
    var right: Int64 = 0
    for (left in 0..n) {
        while (right < n && inversions < k) {
            let pos = lowerBound(values, m, a[right]) + 1
            inversions += windowSize - bitSum(tree, pos)
            bitAdd(tree, m, pos, 1)
            windowSize += 1
            right += 1
        }
        if (inversions >= k) {
            answer += n - right + 1
        }
        let pos = lowerBound(values, m, a[left]) + 1
        inversions -= bitSum(tree, pos - 1)
        bitAdd(tree, m, pos, -1)
        windowSize -= 1
    }
    return answer
}
