package t20_prime_count

import std.collection.*

func solve(n: Int64, a: Array<Int64>): Array<Int64> {
    var limit = 0
    for (x in a) {
        if (x > limit) {
            limit = x
        }
    }
    let sieve = Array<Bool>(limit + 1, repeat: true)
    sieve[0] = false
    if (limit >= 1) {
        sieve[1] = false
    }
    var p = 2
    while (p * p <= limit) {
        if (sieve[p]) {
            var j = p * p
            while (j <= limit) {
                sieve[j] = false
                j += p
            }
        }
        p += 1
    }
    let primes = ArrayList<Int64>()
    for (k in 0..(limit + 1)) {
        if (sieve[k]) {
            primes.add(k)
        }
    }
    let total = primes.size
    let answer = Array<Int64>(n, repeat: 0)
    for (k in 0..n) {
        let x = a[k]
        var lo = 0
        var hi = total
        while (lo < hi) {
            let mid = (lo + hi) / 2
            if (primes[mid] <= x) {
                lo = mid + 1
            } else {
                hi = mid
            }
        }
        answer[k] = lo
    }
    return answer
}
