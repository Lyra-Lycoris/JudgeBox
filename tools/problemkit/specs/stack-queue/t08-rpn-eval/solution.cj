package t08_rpn_eval

func parseNumber(text: String): Int64 {
    let chars = text.toRuneArray()
    var index = 0
    var sign = 1
    if (chars[0] == r'-') {
        sign = -1
        index = 1
    }
    var value = 0
    while (index < chars.size) {
        value = value * 10 + Int64(UInt32(chars[index]) - UInt32(r'0'))
        index += 1
    }
    return sign * value
}

func truncDiv(a: Int64, b: Int64): Int64 {
    let absA = if (a < 0) {
        -a
    } else {
        a
    }
    let absB = if (b < 0) {
        -b
    } else {
        b
    }
    let quotient = absA / absB
    if ((a < 0) == (b < 0)) {
        return quotient
    }
    return -quotient
}

func solve(k: Int64, tokens: Array<String>): Int64 {
    let stack = Array<Int64>(k / 2 + 2, repeat: 0)
    var top = 0
    for (token in tokens) {
        let first = token.toRuneArray()[0]
        if (token.size == 1 && (first == r'+' || first == r'-' || first == r'*' || first == r'/')) {
            let b = stack[top - 1]
            let a = stack[top - 2]
            var result = 0
            if (first == r'+') {
                result = a + b
            } else if (first == r'-') {
                result = a - b
            } else if (first == r'*') {
                result = a * b
            } else {
                result = truncDiv(a, b)
            }
            stack[top - 2] = result
            top -= 1
        } else {
            stack[top] = parseNumber(token)
            top += 1
        }
    }
    return stack[top - 1]
}
