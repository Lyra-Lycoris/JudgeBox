package t01_expr_eval

func precedenceOf(code: Int64): Int64 {
    if (code == 42 || code == 47) {
        return 2
    }
    return 1
}

func applyTop(values: Array<Int64>, valueTop: Int64, ops: Array<Int64>, opTop: Int64): Int64 {
    let op = ops[opTop - 1]
    let b = values[valueTop - 1]
    let a = values[valueTop - 2]
    var result = 0
    if (op == 43) {
        result = a + b
    } else if (op == 45) {
        result = a - b
    } else if (op == 42) {
        result = a * b
    } else {
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
            result = quotient
        } else {
            result = -quotient
        }
    }
    values[valueTop - 2] = result
    return valueTop - 1
}

func solve(expr: String): Int64 {
    let chars = expr.toRuneArray()
    let total = chars.size
    let values = Array<Int64>(total + 2, repeat: 0)
    let ops = Array<Int64>(total + 2, repeat: 0)
    var valueTop = 0
    var opTop = 0
    var index = 0
    while (index < total) {
        let code = Int64(UInt32(chars[index]))
        if (code >= 48 && code <= 57) {
            var number = 0
            while (index < total) {
                let digit = Int64(UInt32(chars[index]))
                if (digit < 48 || digit > 57) {
                    break
                }
                number = number * 10 + (digit - 48)
                index += 1
            }
            values[valueTop] = number
            valueTop += 1
            continue
        }
        if (code == 40) {
            ops[opTop] = code
            opTop += 1
        } else if (code == 41) {
            while (ops[opTop - 1] != 40) {
                valueTop = applyTop(values, valueTop, ops, opTop)
                opTop -= 1
            }
            opTop -= 1
        } else {
            while (opTop > 0 && ops[opTop - 1] != 40 && precedenceOf(ops[opTop - 1]) >= precedenceOf(code)) {
                valueTop = applyTop(values, valueTop, ops, opTop)
                opTop -= 1
            }
            ops[opTop] = code
            opTop += 1
        }
        index += 1
    }
    while (opTop > 0) {
        valueTop = applyTop(values, valueTop, ops, opTop)
        opTop -= 1
    }
    return values[0]
}
