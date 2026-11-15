package t22_two_single_numbers

func solve(n: Int64, a: Array<Int64>): Array<Int64> {
    var x: Int64 = 0
    for (v in a) {
        x = x ^ v
    }
    let lowbit = x & (-x)
    var p: Int64 = 0
    var q: Int64 = 0
    for (v in a) {
        if ((v & lowbit) != 0) {
            p = p ^ v
        } else {
            q = q ^ v
        }
    }
    let answer = Array<Int64>(2, repeat: 0)
    if (p < q) {
        answer[0] = p
        answer[1] = q
    } else {
        answer[0] = q
        answer[1] = p
    }
    return answer
}
