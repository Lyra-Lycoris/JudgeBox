package t08_valid_parentheses

func solve(s: String): Bool {
    let chars = s.toRuneArray()
    let stack = Array<Int64>(chars.size + 1, repeat: 0)
    var top = 0
    for (ch in chars) {
        let code = Int64(UInt32(ch))
        if (code == 40) {
            stack[top] = 41
            top += 1
        } else if (code == 91) {
            stack[top] = 93
            top += 1
        } else if (code == 123) {
            stack[top] = 125
            top += 1
        } else {
            if (top == 0 || stack[top - 1] != code) {
                return false
            }
            top -= 1
        }
    }
    return top == 0
}
