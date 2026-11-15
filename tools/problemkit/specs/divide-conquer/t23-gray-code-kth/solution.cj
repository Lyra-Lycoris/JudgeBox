package t23_gray_code_kth

func gray(bits: Int64, index: Int64): Int64 {
    if (bits == 0) {
        return 0
    }
    let half = 1 << (bits - 1)
    if (index < half) {
        return gray(bits - 1, index)
    }
    return half + gray(bits - 1, 2 * half - 1 - index)
}

func solve(n: Int64, k: Int64): Int64 {
    return gray(n, k)
}
