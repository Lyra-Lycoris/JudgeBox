package t03_gas_station

func solve(n: Int64, gas: Array<Int64>, cost: Array<Int64>): Int64 {
    var total = 0
    for (i in 0..n) {
        total += gas[i] - cost[i]
    }
    if (total < 0) {
        return -1
    }
    var start = 0
    var tank = 0
    for (i in 0..n) {
        tank += gas[i] - cost[i]
        if (tank < 0) {
            start = i + 1
            tank = 0
        }
    }
    return start
}
