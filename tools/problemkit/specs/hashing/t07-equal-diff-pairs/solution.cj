package t07_equal_diff_pairs

import std.collection.*

func solve(n: Int64, a: Array<Int64>): Int64 {
    let diffCounts = HashMap<Int64, Int64>()
    let sumCounts = HashMap<Int64, Int64>()
    var answer = 0
    for (i in 0..n) {
        let index = i + 1
        let diffKey = a[i] - index
        if (diffCounts.contains(diffKey)) {
            answer += diffCounts[diffKey]
            diffCounts[diffKey] = diffCounts[diffKey] + 1
        } else {
            diffCounts[diffKey] = 1
        }
        let sumKey = a[i] + index
        if (sumCounts.contains(sumKey)) {
            answer += sumCounts[sumKey]
            sumCounts[sumKey] = sumCounts[sumKey] + 1
        } else {
            sumCounts[sumKey] = 1
        }
    }
    return answer
}
