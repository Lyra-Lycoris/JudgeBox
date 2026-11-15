package t15_subtree_size

func solve(n: Int64, p: Array<Int64>): Array<Int64> {
    let size = Array<Int64>(n + 1, repeat: 1)
    size[0] = 0
    var v = n
    while (v >= 2) {
        size[p[v - 2]] += size[v]
        v -= 1
    }
    let answer = Array<Int64>(n, repeat: 0)
    for (i in 1..(n + 1)) {
        answer[i - 1] = size[i]
    }
    return answer
}
