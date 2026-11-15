package t12_rle_substring_length

func encodedCost(length: Int64): Int64 {
    if (length <= 1) {
        return 1
    }
    var value = length
    var digits: Int64 = 0
    while (value > 0) {
        digits += 1
        value /= 10
    }
    return 1 + digits
}

func solve(n: Int64, s: String, q: Int64, qs: Array<Array<Int64>>): Array<Int64> {
    let chars = s.toRuneArray()
    let m = chars.size
    let runEnd = Array<Int64>(m + 1, repeat: 0)
    let prefix = Array<Int64>(m + 2, repeat: 0)
    var runs: Int64 = 0
    var index: Int64 = 0
    while (index < m) {
        var j = index + 1
        while (j < m && chars[j] == chars[index]) {
            j += 1
        }
        runEnd[runs] = j
        runs += 1
        prefix[runs] = prefix[runs - 1] + encodedCost(j - index)
        index = j
    }
    let answer = Array<Int64>(q, repeat: 0)
    for (k in 0..q) {
        let left = qs[k][0]
        let right = qs[k][1]
        var low: Int64 = 0
        var high: Int64 = runs
        while (low < high) {
            let mid = (low + high) / 2
            if (runEnd[mid] <= left - 1) {
                low = mid + 1
            } else {
                high = mid
            }
        }
        let lowIndex = low
        low = 0
        high = runs
        while (low < high) {
            let mid = (low + high) / 2
            if (runEnd[mid] <= right - 1) {
                low = mid + 1
            } else {
                high = mid
            }
        }
        let highIndex = low
        if (lowIndex == highIndex) {
            answer[k] = encodedCost(right - left + 1)
        } else {
            let total = encodedCost(runEnd[lowIndex] - (left - 1)) + encodedCost(right - runEnd[highIndex - 1]) + prefix[highIndex] - prefix[lowIndex + 1]
            answer[k] = total
        }
    }
    return answer
}
