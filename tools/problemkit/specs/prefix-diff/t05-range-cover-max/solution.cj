package t05_range_cover_max

func solve(n: Int64, q: Int64, segs: Array<Array<Int64>>): Array<Int64> {
    let diff = Array<Int64>(n + 1, repeat: 0)
    for (i in 0..q) {
        let l = segs[i][0]
        let r = segs[i][1]
        diff[l - 1] = diff[l - 1] + 1
        diff[r] = diff[r] - 1
    }
    var cur: Int64 = 0
    var best: Int64 = -1
    var bestPos: Int64 = 1
    for (i in 0..n) {
        cur = cur + diff[i]
        if (cur > best) {
            best = cur
            bestPos = i + 1
        }
    }
    return [best, bestPos]
}
