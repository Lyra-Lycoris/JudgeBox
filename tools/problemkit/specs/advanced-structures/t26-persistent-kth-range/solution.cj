package t26_persistent_kth_range

import std.sort.*

func kthLowerBound(arr: Array<Int64>, len: Int64, x: Int64): Int64 {
    var lo: Int64 = 0
    var hi = len
    while (lo < hi) {
        let mid = lo + (hi - lo) / 2
        if (arr[mid] < x) {
            lo = mid + 1
        } else {
            hi = mid
        }
    }
    return lo
}

func solve(n: Int64, a: Array<Int64>, m: Int64, queries: Array<Array<Int64>>): Array<Int64> {
    let values = a.clone()
    sort(values)
    var uniq: Int64 = 0
    for (i in 0..n) {
        if (i == 0 || values[i] != values[i - 1]) {
            values[uniq] = values[i]
            uniq += 1
        }
    }

    var depth: Int64 = 1
    while ((1 << depth) < uniq) {
        depth += 1
    }
    let maxNodes = n * (depth + 1) + 2
    let leftChild = Array<Int64>(maxNodes, repeat: 0)
    let rightChild = Array<Int64>(maxNodes, repeat: 0)
    let total = Array<Int64>(maxNodes, repeat: 0)
    let root = Array<Int64>(n + 1, repeat: 0)
    var nodes: Int64 = 0

    for (i in 0..n) {
        let pos = kthLowerBound(values, uniq, a[i])
        let prev = root[i]
        nodes += 1
        let node = nodes
        total[node] = total[prev] + 1
        leftChild[node] = leftChild[prev]
        rightChild[node] = rightChild[prev]
        root[i + 1] = node

        var lo: Int64 = 0
        var hi = uniq - 1
        var curNew = node
        var curOld = prev
        while (lo < hi) {
            let mid = (lo + hi) / 2
            nodes += 1
            let child = nodes
            if (pos <= mid) {
                let oldChild = leftChild[curOld]
                total[child] = total[oldChild] + 1
                leftChild[child] = leftChild[oldChild]
                rightChild[child] = rightChild[oldChild]
                leftChild[curNew] = child
                curNew = child
                curOld = oldChild
                hi = mid
            } else {
                let oldChild = rightChild[curOld]
                total[child] = total[oldChild] + 1
                leftChild[child] = leftChild[oldChild]
                rightChild[child] = rightChild[oldChild]
                rightChild[curNew] = child
                curNew = child
                curOld = oldChild
                lo = mid + 1
            }
        }
    }

    let answer = Array<Int64>(m, repeat: 0)
    for (t in 0..m) {
        let l = queries[t][0]
        let r = queries[t][1]
        var k = queries[t][2]
        var rootR = root[r]
        var rootL = root[l - 1]
        var lo: Int64 = 0
        var hi = uniq - 1
        while (lo < hi) {
            let mid = (lo + hi) / 2
            let leftCount = total[leftChild[rootR]] - total[leftChild[rootL]]
            if (k <= leftCount) {
                rootR = leftChild[rootR]
                rootL = leftChild[rootL]
                hi = mid
            } else {
                k = k - leftCount
                rootR = rightChild[rootR]
                rootL = rightChild[rootL]
                lo = mid + 1
            }
        }
        answer[t] = values[lo]
    }
    return answer
}
