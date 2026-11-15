package t05_range_sum_queries

func solve(n: Int64, a: Array<Int64>, l: Int64, r: Int64): Int64 {
    let pre = Array<Int64>(n + 1, repeat: 0)
    for (i in 0..n) {
        pre[i + 1] = pre[i] + a[i]
    }
    return pre[r] - pre[l - 1]
}
