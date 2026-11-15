package proto_array_sum

func solve(n: Int64, a: Array<Int64>): Int64 {
    var sum = 0
    for (x in a) {
        sum += x
    }
    return sum
}
