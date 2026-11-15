package t23_memo_fib

let FIB_MOD: Int64 = 1000000007

var gFibA: Int64 = 0
var gFibB: Int64 = 1

func fibPair(n: Int64): Unit {
    if (n == 0) {
        gFibA = 0
        gFibB = 1
        return
    }
    fibPair(n >> 1)
    let a = gFibA
    let b = gFibB
    let c = a * ((2 * b - a + FIB_MOD) % FIB_MOD) % FIB_MOD
    let d = (a * a + b * b) % FIB_MOD
    if ((n & 1) == 1) {
        gFibA = d
        gFibB = (c + d) % FIB_MOD
    } else {
        gFibA = c
        gFibB = d
    }
}

func solve(n: Int64): Int64 {
    fibPair(n)
    return gFibA
}
