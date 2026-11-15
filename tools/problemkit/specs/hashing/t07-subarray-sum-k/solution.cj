package t07_subarray_sum_k

import std.collection.*

func solve(n: Int64, k: Int64, a: Array<Int64>): Int64 {
    let counts = HashMap<Int64, Int64>()
    counts[0] = 1
    var prefix = 0
    var answer = 0
    for (x in a) {
        prefix += x
        let wanted = prefix - k
        if (counts.contains(wanted)) {
            answer += counts[wanted]
        }
        if (counts.contains(prefix)) {
            counts[prefix] = counts[prefix] + 1
        } else {
            counts[prefix] = 1
        }
    }
    return answer
}
