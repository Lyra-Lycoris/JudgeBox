package t24_polygon_area2

func solve(n: Int64, xs: Array<Int64>, ys: Array<Int64>): Int64 {
    var total: Int64 = 0
    var px = xs[n - 1]
    var py = ys[n - 1]
    for (i in 0..n) {
        let cx = xs[i]
        let cy = ys[i]
        total += px * cy - cx * py
        px = cx
        py = cy
    }
    if (total < 0) {
        total = -total
    }
    return total
}
