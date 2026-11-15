package t06_two_sum_sorted_count

func solve(n: Int64, target: Int64, a: Array<Int64>): Int64 {
    var i: Int64 = 0
    var j: Int64 = n - 1
    var count: Int64 = 0
    while (i < j) {
        let sum = a[i] + a[j]
        if (sum < target) {
            i += 1
        } else if (sum > target) {
            j -= 1
        } else {
            if (a[i] == a[j]) {
                let m = j - i + 1
                count += m * (m - 1) / 2
                break
            }
            var leftCount: Int64 = 1
            while (i + leftCount < j && a[i + leftCount] == a[i]) {
                leftCount += 1
            }
            var rightCount: Int64 = 1
            while (j - rightCount > i && a[j - rightCount] == a[j]) {
                rightCount += 1
            }
            count += leftCount * rightCount
            i += leftCount
            j -= rightCount
        }
    }
    return count
}
