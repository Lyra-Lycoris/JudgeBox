package t21_coprime_count

func solve(n: Int64, m: Int64): Int64 {
    let primes = Array<Int64>(64, repeat: 0)
    var k: Int64 = 0
    var x = m
    if (x % 2 == 0) {
        primes[k] = 2
        k += 1
        while (x % 2 == 0) {
            x = x / 2
        }
    }
    var d: Int64 = 3
    while (d * d <= x) {
        if (x % d == 0) {
            primes[k] = d
            k += 1
            while (x % d == 0) {
                x = x / d
            }
        }
        d += 2
    }
    if (x > 1) {
        primes[k] = x
        k += 1
    }
    var answer: Int64 = 0
    for (mask in 0..(1 << k)) {
        var product: Int64 = 1
        var bits: Int64 = 0
        for (j in 0..k) {
            if (((mask >> j) & 1) == 1) {
                product = product * primes[j]
                bits += 1
            }
        }
        let term = n / product
        if (bits % 2 == 0) {
            answer += term
        } else {
            answer -= term
        }
    }
    return answer
}
