package t16_max_product_subarray

func solve(n: Int64, a: Array<Int64>): Int64 {
    var best = a[0]
    var mx = a[0]
    var mn = a[0]
    for (i in 1..n) {
        let x = a[i]
        let c1 = mx * x
        let c2 = mn * x
        var newMax = x
        if (c1 > newMax) {
            newMax = c1
        }
        if (c2 > newMax) {
            newMax = c2
        }
        var newMin = x
        if (c1 < newMin) {
            newMin = c1
        }
        if (c2 < newMin) {
            newMin = c2
        }
        mx = newMax
        mn = newMin
        if (mx > best) {
            best = mx
        }
    }
    return best
}
