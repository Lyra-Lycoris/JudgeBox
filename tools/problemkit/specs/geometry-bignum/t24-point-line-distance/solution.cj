package t24_point_line_distance

func solve(x1: Int64, y1: Int64, x2: Int64, y2: Int64, px: Int64, py: Int64, d: Int64): Bool {
    let dx = x2 - x1
    let dy = y2 - y1
    let cross = dx * (py - y1) - dy * (px - x1)
    let len2 = dx * dx + dy * dy
    return cross * cross <= d * d * len2
}
