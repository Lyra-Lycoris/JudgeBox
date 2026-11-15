package t05_bracket_substrings

func solve(s: String): Int64 {
    let runes = s.toRuneArray()
    let n = runes.size
    let counts = Array<Int64>(2 * n + 1, repeat: 0)
    let stack = Array<Int64>(n + 1, repeat: 0)
    var top: Int64 = 1
    var prefix: Int64 = 0
    var answer: Int64 = 0
    counts[n] = 1
    stack[0] = 0
    for (r in runes) {
        if (r == r'(') {
            prefix = prefix + 1
        } else {
            prefix = prefix - 1
        }
        while (top > 0 && stack[top - 1] > prefix) {
            counts[stack[top - 1] + n] = 0
            top = top - 1
        }
        answer = answer + counts[prefix + n]
        counts[prefix + n] = counts[prefix + n] + 1
        if (top == 0 || stack[top - 1] < prefix) {
            stack[top] = prefix
            top = top + 1
        }
    }
    return answer
}
