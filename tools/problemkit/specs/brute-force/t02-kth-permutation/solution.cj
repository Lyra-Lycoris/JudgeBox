package t02_kth_permutation

func solve(n: Int64, k: Int64): Array<Int64> {
    let p = Array<Int64>(n, repeat: 0)
    for (i in 0..n) {
        p[i] = i + 1
    }
    var step: Int64 = 1
    while (step < k) {
        var i = n - 2
        while (i >= 0 && p[i] >= p[i + 1]) {
            i -= 1
        }
        if (i < 0) {
            break
        }
        var j = n - 1
        while (p[j] <= p[i]) {
            j -= 1
        }
        let t = p[i]
        p[i] = p[j]
        p[j] = t
        var l = i + 1
        var r = n - 1
        while (l < r) {
            let tmp = p[l]
            p[l] = p[r]
            p[r] = tmp
            l += 1
            r -= 1
        }
        step += 1
    }
    return p
}
