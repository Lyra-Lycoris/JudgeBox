package t16_lis_len

func solve(n: Int64, a: Array<Int64>): Int64 {
    let tails = Array<Int64>(n, repeat: 0)
    var length: Int64 = 0
    for (i in 0..n) {
        let x = a[i]
        var lo: Int64 = 0
        var hi = length
        while (lo < hi) {
            let mid = (lo + hi) / 2
            if (tails[mid] < x) {
                lo = mid + 1
            } else {
                hi = mid
            }
        }
        tails[lo] = x
        if (lo == length) {
            length += 1
        }
    }
    return length
}
