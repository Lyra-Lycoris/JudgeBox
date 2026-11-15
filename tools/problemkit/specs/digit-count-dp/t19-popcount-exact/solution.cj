package t19_popcount_exact

func countPopUpTo(x: Int64, k: Int64, comb: Array<Array<Int64>>): Int64 {
    if (x < 0 || k < 0) {
        return 0
    }
    var res: Int64 = 0
    var used: Int64 = 0
    var ok = true
    var bit: Int64 = 60
    while (bit >= 0) {
        if (((x >> bit) & 1) != 0) {
            let need = k - used
            if (need >= 0 && need <= bit) {
                res += comb[bit][need]
            }
            used += 1
            if (used > k) {
                ok = false
                break
            }
        }
        bit -= 1
    }
    if (ok && used == k) {
        res += 1
    }
    return res
}

func solve(l: Int64, r: Int64, k: Int64): Int64 {
    let comb = Array<Array<Int64>>(62, { _ => Array<Int64>(62, repeat: 0) })
    for (i in 0..62) {
        comb[i][0] = 1
        for (j in 1..(i + 1)) {
            comb[i][j] = comb[i - 1][j - 1] + comb[i - 1][j]
        }
    }
    return countPopUpTo(r, k, comb) - countPopUpTo(l - 1, k, comb)
}
