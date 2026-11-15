package t22_next_palindrome

import std.collection.*
import std.convert.Parsable

func mirror(half: String, keep: Int64): String {
    let chars = half.toRuneArray()
    let sb = StringBuilder()
    sb.append(half)
    var i = keep - 1
    while (i >= 0) {
        sb.append(chars[i].toString())
        i -= 1
    }
    return sb.toString()
}

func solve(n: Int64): Int64 {
    if (n < 10) {
        return n
    }
    let s = n.toString()
    let chars = s.toRuneArray()
    let L = chars.size
    let halfLen = (L + 1) / 2
    let sb = StringBuilder()
    for (i in 0..halfLen) {
        sb.append(chars[i].toString())
    }
    let half = sb.toString()
    let candidate = Int64.parse(mirror(half, L / 2))
    if (candidate >= n) {
        return candidate
    }
    let next = (Int64.parse(half) + 1).toString()
    if (next.toRuneArray().size > halfLen) {
        let answer = StringBuilder()
        answer.append("1")
        for (i in 0..(L - 1)) {
            answer.append("0")
        }
        answer.append("1")
        return Int64.parse(answer.toString())
    }
    return Int64.parse(mirror(next, L / 2))
}
