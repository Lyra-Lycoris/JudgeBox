package t02_max_ones_rect

func solve(n: Int64, m: Int64, g: Array<Array<Int64>>): Int64 {
    var best: Int64 = 0
    let heights = Array<Int64>(m, repeat: 0)
    let st = Array<Int64>(m + 1, repeat: 0)
    var top: Int64 = 0
    while (top < n) {
        for (c in 0..m) {
            heights[c] = 0
        }
        var bottom = top
        while (bottom < n) {
            for (c in 0..m) {
                if (g[bottom][c] != 0) {
                    heights[c] += 1
                } else {
                    heights[c] = 0
                }
            }
            var sp: Int64 = 0
            var c: Int64 = 0
            while (c <= m) {
                var h: Int64 = 0
                if (c < m) {
                    h = heights[c]
                }
                while (sp > 0 && heights[st[sp - 1]] >= h) {
                    let ph = heights[st[sp - 1]]
                    sp -= 1
                    var left: Int64 = -1
                    if (sp > 0) {
                        left = st[sp - 1]
                    }
                    let area = ph * (c - left - 1)
                    if (area > best) {
                        best = area
                    }
                }
                st[sp] = c
                sp += 1
                c += 1
            }
            bottom += 1
        }
        top += 1
    }
    return best
}
