package t16_max_nonadjacent

func solve(n: Int64, a: Array<Int64>): Int64 {
    var notTake: Int64 = 0
    var take: Int64 = a[0]
    for (i in 1..n) {
        let newTake = notTake + a[i]
        var newNot = notTake
        if (take > newNot) {
            newNot = take
        }
        notTake = newNot
        take = newTake
    }
    if (take > notTake) {
        return take
    }
    return notTake
}
