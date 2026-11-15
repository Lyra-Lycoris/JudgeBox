package t25_two_sorted_median

func countLE(arr: Array<Int64>, x: Int64): Int64 {
    var lo: Int64 = 0
    var hi: Int64 = arr.size
    while (lo < hi) {
        let mid = (lo + hi) / 2
        if (arr[mid] <= x) {
            lo = mid + 1
        } else {
            hi = mid
        }
    }
    return lo
}

func kthSmallest(a: Array<Int64>, b: Array<Int64>, t: Int64): Int64 {
    var lo: Int64 = -1000000001
    var hi: Int64 = 1000000001
    while (lo < hi) {
        let mid = lo + (hi - lo) / 2
        let cnt = countLE(a, mid) + countLE(b, mid)
        if (cnt >= t) {
            hi = mid
        } else {
            lo = mid + 1
        }
    }
    return lo
}

func solve(n: Int64, a: Array<Int64>, m: Int64, b: Array<Int64>): Int64 {
    let total = n + m
    return kthSmallest(a, b, (total + 1) / 2) + kthSmallest(a, b, (total + 2) / 2)
}
