package t24_convex_hull_count

import std.sort.*

func solve(n: Int64, xs: Array<Int64>, ys: Array<Int64>): Int64 {
    let offset: Int64 = 1000000000
    let mod: Int64 = 2000000001
    var keys = Array<Int64>(n, repeat: 0)
    for (i in 0..n) {
        keys[i] = (xs[i] + offset) * mod + (ys[i] + offset)
    }
    sort(keys)
    var m: Int64 = 0
    for (i in 0..n) {
        if (i == 0 || keys[i] != keys[i - 1]) {
            keys[m] = keys[i]
            m += 1
        }
    }
    if (m <= 2) {
        return m
    }
    var hx = Array<Int64>(m + 1, repeat: 0)
    var hy = Array<Int64>(m + 1, repeat: 0)
    var size: Int64 = 0
    for (i in 0..m) {
        let x = keys[i] / mod - offset
        let y = keys[i] % mod - offset
        while (size >= 2) {
            let ox = hx[size - 2]
            let oy = hy[size - 2]
            let ax = hx[size - 1]
            let ay = hy[size - 1]
            let cr = (ax - ox) * (y - oy) - (ay - oy) * (x - ox)
            if (cr <= 0) {
                size -= 1
            } else {
                break
            }
        }
        hx[size] = x
        hy[size] = y
        size += 1
    }
    let lowerSize = size
    var ux = Array<Int64>(m + 1, repeat: 0)
    var uy = Array<Int64>(m + 1, repeat: 0)
    var upperSize: Int64 = 0
    var i = m - 1
    while (i >= 0) {
        let x = keys[i] / mod - offset
        let y = keys[i] % mod - offset
        while (upperSize >= 2) {
            let ox = ux[upperSize - 2]
            let oy = uy[upperSize - 2]
            let ax = ux[upperSize - 1]
            let ay = uy[upperSize - 1]
            let cr = (ax - ox) * (y - oy) - (ay - oy) * (x - ox)
            if (cr <= 0) {
                upperSize -= 1
            } else {
                break
            }
        }
        ux[upperSize] = x
        uy[upperSize] = y
        upperSize += 1
        i -= 1
    }
    return lowerSize + upperSize - 2
}
