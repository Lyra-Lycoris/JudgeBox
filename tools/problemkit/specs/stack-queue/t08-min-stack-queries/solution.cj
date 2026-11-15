package t08_min_stack_queries

func solve(m: Int64, op: Array<Int64>, val: Array<Int64>): Array<Int64> {
    let stack = Array<Int64>(m, repeat: 0)
    let minimum = Array<Int64>(m, repeat: 0)
    let answer = Array<Int64>(m, repeat: 0)
    var top = 0
    var count = 0
    for (i in 0..m) {
        if (op[i] == 1) {
            let v = val[i]
            stack[top] = v
            if (top == 0) {
                minimum[top] = v
            } else if (v < minimum[top - 1]) {
                minimum[top] = v
            } else {
                minimum[top] = minimum[top - 1]
            }
            top += 1
        } else if (op[i] == 2) {
            top -= 1
        } else {
            answer[count] = minimum[top - 1]
            count += 1
        }
    }
    let result = Array<Int64>(count, repeat: 0)
    for (i in 0..count) {
        result[i] = answer[i]
    }
    return result
}
