package t08_histogram_rect

func solve(n: Int64, h: Array<Int64>): Int64 {
    let stack = Array<Int64>(n + 1, repeat: 0)
    var top = 0
    var best = 0
    var i = 0
    while (i <= n) {
        let cur = if (i < n) {
            h[i]
        } else {
            0
        }
        while (top > 0 && h[stack[top - 1]] >= cur) {
            let height = h[stack[top - 1]]
            top -= 1
            let left = if (top > 0) {
                stack[top - 1]
            } else {
                -1
            }
            let area = height * (i - left - 1)
            if (area > best) {
                best = area
            }
        }
        stack[top] = i
        top += 1
        i += 1
    }
    return best
}
