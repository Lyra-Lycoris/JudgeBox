package t23_median_two_sorted

func kth(a: Array<Int64>, b: Array<Int64>, start: Int64): Int64 {
    var i: Int64 = 0
    var j: Int64 = 0
    var k = start
    let na = a.size
    let nb = b.size
    while (true) {
        if (i == na) {
            return b[j + k]
        }
        if (j == nb) {
            return a[i + k]
        }
        if (k == 0) {
            if (a[i] < b[j]) {
                return a[i]
            }
            return b[j]
        }
        let step = (k + 1) / 2
        var stepA = step
        if (stepA > na - i) {
            stepA = na - i
        }
        var stepB = step
        if (stepB > nb - j) {
            stepB = nb - j
        }
        let ai = i + stepA - 1
        let bj = j + stepB - 1
        if (a[ai] <= b[bj]) {
            k -= ai - i + 1
            i = ai + 1
        } else {
            k -= bj - j + 1
            j = bj + 1
        }
    }
    return 0
}

func solve(n: Int64, a: Array<Int64>, m: Int64, b: Array<Int64>): Int64 {
    let total = n + m
    return kth(a, b, (total - 1) / 2) + kth(a, b, total / 2)
}
