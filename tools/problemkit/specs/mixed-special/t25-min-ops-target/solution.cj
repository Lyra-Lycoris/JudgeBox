package t25_min_ops_target

func solve(n: Int64, a: Array<Int64>, b: Array<Int64>): Int64 {
    var answer: Int64 = 0
    var prevPos: Int64 = 0
    var prevNeg: Int64 = 0
    for (i in 0..n) {
        let d = b[i] - a[i]
        var pos: Int64 = 0
        var neg: Int64 = 0
        if (d > 0) {
            pos = d
        } else {
            neg = -d
        }
        if (pos > prevPos) {
            answer += pos - prevPos
        }
        if (neg > prevNeg) {
            answer += neg - prevNeg
        }
        prevPos = pos
        prevNeg = neg
    }
    return answer
}
