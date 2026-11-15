package t05_max_subarray_sum

func solve(n: Int64, a: Array<Int64>): Int64 {
    var best = a[0]
    var prefix: Int64 = 0
    var minPrefix: Int64 = 0
    for (x in a) {
        prefix = prefix + x
        let candidate = prefix - minPrefix
        if (candidate > best) {
            best = candidate
        }
        if (prefix < minPrefix) {
            minPrefix = prefix
        }
    }
    return best
}
