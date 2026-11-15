package t25_k_positive_sum

func solve(s: Int64, k: Int64): Array<Int64> {
    let v = Array<Int64>(k, repeat: 1)
    v[k - 1] = s - (k - 1)
    return v
}
