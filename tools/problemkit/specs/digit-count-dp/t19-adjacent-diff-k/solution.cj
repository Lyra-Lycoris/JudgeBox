package t19_adjacent_diff_k

func tailCount(rem: Int64, last: Int64, cnt: Array<Array<Int64>>): Int64 {
    return cnt[rem][last]
}

func countUpTo(x: Int64, k: Int64, cnt: Array<Array<Int64>>): Int64 {
    if (x <= 0) {
        return 0
    }
    let digits = Array<Int64>(20, repeat: 0)
    var len: Int64 = 0
    var t = x
    while (true) {
        digits[len] = t % 10
        len += 1
        t = t / 10
        if (t == 0) {
            break
        }
    }
    var res: Int64 = 0
    var length: Int64 = 1
    while (length < len) {
        var first: Int64 = 1
        while (first <= 9) {
            res += tailCount(length - 1, first, cnt)
            first += 1
        }
        length += 1
    }
    var pos = len - 1
    while (pos >= 0) {
        let cur = digits[pos]
        var lo: Int64 = 0
        if (pos == len - 1) {
            lo = 1
        }
        var v = lo
        while (v < cur) {
            var good = true
            if (pos < len - 1) {
                let diff = v - digits[pos + 1]
                if (diff > k || -diff > k) {
                    good = false
                }
            }
            if (good) {
                res += tailCount(pos, v, cnt)
            }
            v += 1
        }
        if (pos < len - 1) {
            let diff = cur - digits[pos + 1]
            if (diff > k || -diff > k) {
                return res
            }
        }
        pos -= 1
    }
    return res + 1
}

func solve(l: Int64, r: Int64, k: Int64): Int64 {
    let cnt = Array<Array<Int64>>(19, { _ => Array<Int64>(10, repeat: 0) })
    var last: Int64 = 0
    while (last < 10) {
        cnt[0][last] = 1
        last += 1
    }
    var rem: Int64 = 1
    while (rem < 19) {
        var ls: Int64 = 0
        while (ls < 10) {
            var sum: Int64 = 0
            var v: Int64 = 0
            while (v < 10) {
                let diff = v - ls
                if (diff <= k && -diff <= k) {
                    sum += cnt[rem - 1][v]
                }
                v += 1
            }
            cnt[rem][ls] = sum
            ls += 1
        }
        rem += 1
    }
    return countUpTo(r, k, cnt) - countUpTo(l - 1, k, cnt)
}
