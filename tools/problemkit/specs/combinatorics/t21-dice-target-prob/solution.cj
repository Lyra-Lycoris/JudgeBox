package t21_dice_target_prob

func solve(n: Int64): Int64 {
    let MOD: Int64 = 1000000007
    let INV6: Int64 = 166666668
    let p = Array<Int64>(n + 1, repeat: 0)
    let pre = Array<Int64>(n + 1, repeat: 0)
    p[0] = 1
    pre[0] = 1
    var i: Int64 = 1
    while (i <= n) {
        var window = pre[i - 1]
        if (i >= 7) {
            window = window - pre[i - 7]
        }
        window = window % MOD
        if (window < 0) {
            window = window + MOD
        }
        p[i] = window * INV6 % MOD
        pre[i] = (pre[i - 1] + p[i]) % MOD
        i += 1
    }
    return p[n]
}
