package t08_next_greater

func solve(n: Int64, a: Array<Int64>): Array<Int64> {
    let answer = Array<Int64>(n, repeat: -1)
    let stack = Array<Int64>(n, repeat: 0)
    var top = 0
    var i = n - 1
    while (i >= 0) {
        while (top > 0 && stack[top - 1] <= a[i]) {
            top -= 1
        }
        if (top > 0) {
            answer[i] = stack[top - 1]
        }
        stack[top] = a[i]
        top += 1
        i -= 1
    }
    return answer
}
