package t28_prefix_inclusion

func popCount(x0: Int64): Int64 {
    var x = x0
    var count: Int64 = 0
    while (x > 0) {
        x = x & (x - 1)
        count += 1
    }
    return count
}

func countUpto(n: Int64, zeroMask: Int64, oneMask: Int64): Int64 {
    if ((zeroMask & oneMask) != 0) {
        return 0
    }
    let both = zeroMask | oneMask
    var total: Int64 = 0
    var ok = true
    var i: Int64 = 59
    while (i >= 0) {
        let nb = (n >> i) & 1
        let forcedOne = (oneMask >> i) & 1
        if (forcedOne == 1) {
            if (nb == 0) {
                ok = false
                break
            }
        } else if (nb == 1) {
            let lowMask = (1 << i) - 1
            let freeBits = i - popCount(both & lowMask)
            total += (1 << freeBits)
            if (((zeroMask >> i) & 1) == 1) {
                ok = false
                break
            }
        }
        i -= 1
    }
    if (ok) {
        total += 1
    }
    if (oneMask == 0) {
        total -= 1
    }
    return total
}

func solve(n: Int64, m: Int64, cond: Array<Array<Int64>>): Int64 {
    let groups = Array<Int64>(m + 1, repeat: 0)
    let masks: Int64 = 1 << m
    var mask: Int64 = 1
    while (mask < masks) {
        var zeroMask: Int64 = 0
        var oneMask: Int64 = 0
        var size: Int64 = 0
        var i: Int64 = 0
        while (i < m) {
            if (((mask >> i) & 1) == 1) {
                size += 1
                let t = cond[i][0]
                let x = cond[i][1]
                if (t == 1) {
                    zeroMask = zeroMask | (x - 1)
                } else {
                    oneMask = oneMask | (1 << x)
                }
            }
            i += 1
        }
        if ((zeroMask & oneMask) == 0) {
            groups[size] += countUpto(n, zeroMask, oneMask)
        }
        mask += 1
    }
    var answer: Int64 = 0
    var size: Int64 = 1
    while (size <= m) {
        if (size % 2 == 1) {
            answer += groups[size]
        } else {
            answer -= groups[size]
        }
        size += 1
    }
    return answer
}
