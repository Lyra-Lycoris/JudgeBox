package t27_slope_opt_partition

// 比较 a*b 与 c*d（四个参数都非负），要求乘积不超过 2^90。
// 仓颉没有 128 位整数，这里用 30 位一段的手工乘法实现。
func __cmpMul(a: Int64, b: Int64, c: Int64, d: Int64): Int64 {
    let MASK: Int64 = 1073741823
    let SH: Int64 = 30
    let a1 = a >> SH
    let a0 = a & MASK
    let b1 = b >> SH
    let b0 = b & MASK
    let p0 = a0 * b0
    let t = a1 * b0 + a0 * b1 + (p0 >> SH)
    let lo1 = p0 & MASK
    let mid1 = t & MASK
    let hi1 = a1 * b1 + (t >> SH)
    let c1 = c >> SH
    let c0 = c & MASK
    let d1 = d >> SH
    let d0 = d & MASK
    let q0 = c0 * d0
    let u = c1 * d0 + c0 * d1 + (q0 >> SH)
    let lo2 = q0 & MASK
    let mid2 = u & MASK
    let hi2 = c1 * d1 + (u >> SH)
    if (hi1 != hi2) {
        if (hi1 > hi2) {
            return 1
        }
        return -1
    }
    if (mid1 != mid2) {
        if (mid1 > mid2) {
            return 1
        }
        return -1
    }
    if (lo1 != lo2) {
        if (lo1 > lo2) {
            return 1
        }
        return -1
    }
    return 0
}

func solve(n: Int64, cost: Int64, a: Array<Int64>): Int64 {
    // 前缀和：S[i] = a[0] + ... + a[i-1]
    let S = Array<Int64>(n + 1, repeat: 0)
    var i: Int64 = 1
    while (i <= n) {
        S[i] = S[i - 1] + a[i - 1]
        i += 1
    }
    let ms = Array<Int64>(n + 2, repeat: 0)
    let bs = Array<Int64>(n + 2, repeat: 0)
    var head: Int64 = 0
    var tail: Int64 = 1
    var answer: Int64 = 0
    i = 1
    while (i <= n) {
        let si = S[i]
        let x = -2 * si
        while (head + 1 < tail) {
            let v1 = ms[head + 1] * x + bs[head + 1]
            let v0 = ms[head] * x + bs[head]
            if (v1 <= v0) {
                head += 1
            } else {
                break
            }
        }
        let best = ms[head] * x + bs[head]
        let dpi = best + si * si + cost
        if (i == n) {
            answer = dpi
        }
        // 加入直线 m = S[i], b = dp[i] + S[i]^2
        let m = si
        let b = dpi + si * si
        while (tail - head >= 2) {
            let m1 = ms[tail - 2]
            let b1 = bs[tail - 2]
            let m2 = ms[tail - 1]
            let b2 = bs[tail - 1]
            // 中间直线冗余： (b2-b1)*(m3-m2) >= (b3-b2)*(m2-m1)
            if (__cmpMul(b2 - b1, m - m2, b - b2, m2 - m1) >= 0) {
                tail -= 1
            } else {
                break
            }
        }
        ms[tail] = m
        bs[tail] = b
        tail += 1
        i += 1
    }
    return answer
}
