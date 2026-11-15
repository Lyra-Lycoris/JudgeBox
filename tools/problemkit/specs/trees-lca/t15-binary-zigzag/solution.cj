package t15_binary_zigzag

func solve(n: Int64, r: Int64, ch: Array<Int64>): Array<Int64> {
    let answer = Array<Int64>(n, repeat: 0)
    var written = 0
    var cur = Array<Int64>(n, repeat: 0)
    var nxt = Array<Int64>(n, repeat: 0)
    var curSize = 1
    cur[0] = r
    var forward = true
    while (curSize > 0) {
        if (forward) {
            for (i in 0..curSize) {
                answer[written] = cur[i]
                written += 1
            }
        } else {
            var i = curSize - 1
            while (i >= 0) {
                answer[written] = cur[i]
                written += 1
                i -= 1
            }
        }
        var nextSize = 0
        for (i in 0..curSize) {
            let v = cur[i]
            let left = ch[2 * (v - 1)]
            let right = ch[2 * (v - 1) + 1]
            if (left != 0) {
                nxt[nextSize] = left
                nextSize += 1
            }
            if (right != 0) {
                nxt[nextSize] = right
                nextSize += 1
            }
        }
        let tmp = cur
        cur = nxt
        nxt = tmp
        curSize = nextSize
        forward = !forward
    }
    return answer
}
