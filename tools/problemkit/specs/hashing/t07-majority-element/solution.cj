package t07_majority_element

func solve(n: Int64, a: Array<Int64>): Int64 {
    var candidate = a[0]
    var balance = 0
    for (x in a) {
        if (balance == 0) {
            candidate = x
        }
        if (x == candidate) {
            balance += 1
        } else {
            balance -= 1
        }
    }
    return candidate
}
