package t16_stock_once

func solve(n: Int64, a: Array<Int64>): Int64 {
    var best: Int64 = 0
    var mn = a[0]
    for (i in 1..n) {
        let profit = a[i] - mn
        if (profit > best) {
            best = profit
        }
        if (a[i] < mn) {
            mn = a[i]
        }
    }
    return best
}
