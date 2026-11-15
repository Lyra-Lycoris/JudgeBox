package t21_expected_inversion_swap

import std.sort.*

func powMod(base: Int64, exp: Int64): Int64 {
    let MOD: Int64 = 1000000007
    var b = base % MOD
    var e = exp
    var result: Int64 = 1
    while (e > 0) {
        if (e % 2 == 1) {
            result = result * b % MOD
        }
        b = b * b % MOD
        e = e / 2
    }
    return result
}

func norm(value: Int64): Int64 {
    let MOD: Int64 = 1000000007
    var r = value % MOD
    if (r < 0) {
        r = r + MOD
    }
    return r
}

func lowerBound(arr: Array<Int64>, len: Int64, x: Int64): Int64 {
    var lo: Int64 = 0
    var hi = len
    while (lo < hi) {
        let mid = lo + (hi - lo) / 2
        if (arr[mid] < x) {
            lo = mid + 1
        } else {
            hi = mid
        }
    }
    return lo
}

func solve(n: Int64, a: Array<Int64>): Int64 {
    let MOD: Int64 = 1000000007
    if (n < 2) {
        return 0
    }
    let uniq = a.clone()
    sort(uniq)
    var m: Int64 = 0
    var i: Int64 = 0
    while (i < n) {
        if (i == 0 || uniq[i] != uniq[i - 1]) {
            uniq[m] = uniq[i]
            m += 1
        }
        i += 1
    }
    let cnt = Array<Int64>(m, repeat: 0)
    let lessCnt = Array<Int64>(m, repeat: 0)
    let greaterCnt = Array<Int64>(m, repeat: 0)
    for (x in a) {
        let idx = lowerBound(uniq, m, x)
        cnt[idx] = cnt[idx] + 1
    }
    var running: Int64 = 0
    for (j in 0..m) {
        lessCnt[j] = running
        running = running + cnt[j]
    }
    for (j in 0..m) {
        greaterCnt[j] = n - lessCnt[j] - cnt[j]
    }
    let tree = Array<Int64>(m + 1, repeat: 0)
    var invCount: Int64 = 0
    var k: Int64 = 0
    while (k < n) {
        let r = lowerBound(uniq, m, a[k]) + 1
        var seen: Int64 = 0
        var p = r
        while (p > 0) {
            seen = seen + tree[p]
            p = p - (p & -p)
        }
        invCount = invCount + k - seen
        p = r
        while (p <= m) {
            tree[p] = tree[p] + 1
            p = p + (p & -p)
        }
        k += 1
    }
    var equalPairs: Int64 = 0
    for (j in 0..m) {
        equalPairs = equalPairs + cnt[j] * (cnt[j] - 1) / 2
    }
    let totalPairs = n * (n - 1) / 2
    let untouched = (n - 2) * (n - 3) / 2
    var total = norm((untouched % MOD) * (invCount % MOD))
    total = norm(total + norm((totalPairs % MOD) - (invCount % MOD) - (equalPairs % MOD)))
    var sumLeft: Int64 = 0
    k = 0
    while (k < n) {
        let idx = lowerBound(uniq, m, a[k])
        sumLeft = norm(sumLeft + norm((k % MOD) * (greaterCnt[idx] % MOD)))
        k += 1
    }
    total = norm(total + sumLeft)
    var sumRight: Int64 = 0
    k = 0
    while (k < n) {
        let idx = lowerBound(uniq, m, a[k])
        sumRight = norm(sumRight + norm(((n - 1 - k) % MOD) * (lessCnt[idx] % MOD)))
        k += 1
    }
    total = norm(total + sumRight)
    total = norm(total - 2 * (invCount % MOD) % MOD)
    return norm(total * powMod(totalPairs % MOD, MOD - 2))
}
