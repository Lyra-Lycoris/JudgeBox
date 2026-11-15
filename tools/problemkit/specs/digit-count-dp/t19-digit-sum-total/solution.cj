package t19_digit_sum_total

func totalUpTo(x: Int64): Int64 {
    if (x < 0) {
        return 0
    }
    let power = Array<Int64>(17, repeat: 1)
    for (i in 1..17) {
        power[i] = power[i - 1] * 10
    }
    let suffix = Array<Int64>(17, repeat: 0)
    for (i in 1..17) {
        suffix[i] = i * 45 * power[i - 1]
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
    var result: Int64 = 0
    var prefix: Int64 = 0
    var pos = length - 1
    while (pos >= 0) {
        let cur = digits[pos]
        var v: Int64 = 0
        while (v < cur) {
            result += (prefix + v) * power[pos] + suffix[pos]
            v += 1
        }
        prefix += cur
        pos -= 1
    }
    return result + prefix
}

func solve(l: Int64, r: Int64): Int64 {
    return totalUpTo(r) - totalUpTo(l - 1)
}
