package t24_collinear_points

func solve(x1: Int64, y1: Int64, x2: Int64, y2: Int64, x3: Int64, y3: Int64): Bool {
    let cross = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
    return cross == 0
}
