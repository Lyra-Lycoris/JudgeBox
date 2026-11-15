package t24_big_add

import std.collection.*

func solve(a: String, b: String): String {
    var i = a.size - 1
    var j = b.size - 1
    var carry = 0
    let digits = ArrayList<Int64>()
    while (i >= 0 || j >= 0 || carry > 0) {
        var total = carry
        if (i >= 0) {
            total += Int64(a[i]) - 48
            i -= 1
        }
        if (j >= 0) {
            total += Int64(b[j]) - 48
            j -= 1
        }
        digits.add(total % 10)
        carry = total / 10
    }
    let sb = StringBuilder()
    var k = digits.size - 1
    while (k >= 0) {
        sb.append(digits[k].toString())
        k -= 1
    }
    return sb.toString()
}
