package proto_sorted

import std.sort.*

func solve(n: Int64, a: Array<Int64>): Array<Int64> {
    let answer = a.clone()
    sort(answer)
    return answer
}
