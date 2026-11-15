package t22_max_gap_between_ones

func solve(n: Int64): Int64 {
    var x = n
    var best: Int64 = 0
    var last: Int64 = -1
    var pos: Int64 = 0
    while (x > 0) {
        if ((x & 1) != 0) {
            if (last >= 0) {
                let gap = pos - last - 1
                if (gap > best) {
                    best = gap
                }
            }
            last = pos
        }
        x = x >> 1
        pos += 1
    }
    return best
}
