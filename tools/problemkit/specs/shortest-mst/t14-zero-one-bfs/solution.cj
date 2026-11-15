package t14_zero_one_bfs

class IntDeque {
    var data: Array<Int64>
    var headIndex: Int64
    var tailIndex: Int64
    var count: Int64

    init(capacity: Int64) {
        data = Array<Int64>(capacity, repeat: 0)
        headIndex = 0
        tailIndex = 0
        count = 0
    }

    func size(): Int64 {
        return count
    }

    func pushBack(value: Int64) {
        growIfNeeded()
        data[tailIndex] = value
        tailIndex = (tailIndex + 1) % data.size
        count += 1
    }

    func pushFront(value: Int64) {
        growIfNeeded()
        headIndex = (headIndex - 1 + data.size) % data.size
        data[headIndex] = value
        count += 1
    }

    func popFront(): Int64 {
        let value = data[headIndex]
        headIndex = (headIndex + 1) % data.size
        count -= 1
        return value
    }

    func growIfNeeded() {
        if (count < data.size) {
            return
        }
        let bigger = Array<Int64>(data.size * 2, repeat: 0)
        var i: Int64 = 0
        while (i < count) {
            bigger[i] = data[(headIndex + i) % data.size]
            i += 1
        }
        data = bigger
        headIndex = 0
        tailIndex = count
    }
}

func solve(n: Int64, m: Int64, g: Array<Array<Int64>>): Int64 {
    let total = n * m
    let cell = Array<Int64>(total, repeat: 0)
    var i: Int64 = 0
    while (i < n) {
        var j: Int64 = 0
        while (j < m) {
            cell[i * m + j] = g[i][j]
            j += 1
        }
        i += 1
    }
    let INF: Int64 = 1 << 30
    let dist = Array<Int64>(total, repeat: INF)
    dist[0] = 0
    let dq = IntDeque(16)
    dq.pushBack(0)
    while (dq.size() > 0) {
        let u = dq.popFront()
        let du = dist[u]
        let r = u / m
        let c = u - r * m
        var k: Int64 = 0
        while (k < 4) {
            var v: Int64 = -1
            if (k == 0 && r > 0) {
                v = u - m
            } else if (k == 1 && r + 1 < n) {
                v = u + m
            } else if (k == 2 && c > 0) {
                v = u - 1
            } else if (k == 3 && c + 1 < m) {
                v = u + 1
            }
            if (v >= 0) {
                let nd = du + cell[v]
                if (nd < dist[v]) {
                    dist[v] = nd
                    if (cell[v] == 0) {
                        dq.pushFront(v)
                    } else {
                        dq.pushBack(v)
                    }
                }
            }
            k += 1
        }
    }
    return dist[total - 1]
}
