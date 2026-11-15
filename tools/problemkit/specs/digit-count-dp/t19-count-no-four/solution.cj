package t19_count_no_four

func countNoFour(x: Int64): Int64 {
    if (x < 0) {
        return 0
    }
    let digits = Array<Int64>(20, repeat: 0)
    var length: Int64 = 0
    var t = x
    while (true) {
        digits[length] = t % 10
        length += 1
        t = t / 10
        if (t == 0) {
            break
        }
    }
    let power = Array<Int64>(21, repeat: 1)
    var pw: Int64 = 1
    while (pw <= length) {
        power[pw] = power[pw - 1] * 9
        pw += 1
    }
    var total: Int64 = 0
    var pos = length - 1
    while (pos >= 0) {
        let cur = digits[pos]
        var smaller: Int64 = 0
        var v: Int64 = 0
        while (v < cur) {
            if (v != 4) {
                smaller += 1
            }
            v += 1
        }
        total += smaller * power[pos]
        if (cur == 4) {
            return total
        }
        pos -= 1
    }
    return total + 1
}

func solve(l: Int64, r: Int64): Int64 {
    return countNoFour(r) - countNoFour(l - 1)
}
