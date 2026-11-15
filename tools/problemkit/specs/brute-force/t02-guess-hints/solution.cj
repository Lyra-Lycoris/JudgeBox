package t02_guess_hints

func solve(n: Int64, k: Int64, guesses: Array<Int64>, exact: Array<Int64>, loose: Array<Int64>): Array<Int64> {
    let gd = Array<Array<Int64>>(k, { _ => Array<Int64>(n, repeat: 0) })
    for (q in 0..k) {
        var v = guesses[q]
        var i = n - 1
        while (i >= 0) {
            gd[q][i] = v % 10
            v /= 10
            i -= 1
        }
    }
    var total: Int64 = 1
    for (_ in 0..n) {
        total *= 10
    }
    var code: Int64 = 0
    while (code < total) {
        var t = code
        let cd = Array<Int64>(n, repeat: 0)
        var i = n - 1
        while (i >= 0) {
            cd[i] = t % 10
            t /= 10
            i -= 1
        }
        var ok = true
        var q: Int64 = 0
        while (q < k && ok) {
            var a: Int64 = 0
            let ca = Array<Int64>(10, repeat: 0)
            let cb = Array<Int64>(10, repeat: 0)
            for (p in 0..n) {
                if (cd[p] == gd[q][p]) {
                    a += 1
                }
                ca[cd[p]] += 1
                cb[gd[q][p]] += 1
            }
            var b: Int64 = 0
            for (d in 0..10) {
                if (ca[d] < cb[d]) {
                    b += ca[d]
                } else {
                    b += cb[d]
                }
            }
            b -= a
            if (a != exact[q] || b != loose[q]) {
                ok = false
            }
            q += 1
        }
        if (ok) {
            return cd
        }
        code += 1
    }
    return Array<Int64>(n, repeat: 0)
}
