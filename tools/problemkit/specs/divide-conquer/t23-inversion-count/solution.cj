package t23_inversion_count

func invMerge(a: Array<Int64>, tmp: Array<Int64>, l: Int64, r: Int64): Int64 {
    if (r - l <= 1) {
        return 0
    }
    let mid = (l + r) / 2
    var total = invMerge(a, tmp, l, mid) + invMerge(a, tmp, mid, r)
    var i = l
    var j = mid
    var k = l
    while (i < mid && j < r) {
        if (a[i] <= a[j]) {
            tmp[k] = a[i]
            i += 1
        } else {
            tmp[k] = a[j]
            j += 1
            total += mid - i
        }
        k += 1
    }
    while (i < mid) {
        tmp[k] = a[i]
        i += 1
        k += 1
    }
    while (j < r) {
        tmp[k] = a[j]
        j += 1
        k += 1
    }
    for (p in l..r) {
        a[p] = tmp[p]
    }
    return total
}

func solve(n: Int64, a: Array<Int64>): Int64 {
    let work = Array<Int64>(n, repeat: 0)
    for (i in 0..n) {
        work[i] = a[i]
    }
    let tmp = Array<Int64>(n, repeat: 0)
    return invMerge(work, tmp, 0, n)
}
