package t14_second_shortest_strict

import std.collection.*

class MinHeap {
    var keys: ArrayList<Int64> = ArrayList<Int64>()
    var ids: ArrayList<Int64> = ArrayList<Int64>()

    init() {}

    func size(): Int64 {
        return keys.size
    }

    func topKey(): Int64 {
        return keys[0]
    }

    func topId(): Int64 {
        return ids[0]
    }

    func push(key: Int64, id: Int64) {
        keys.add(key)
        ids.add(id)
        var i = keys.size - 1
        while (i > 0) {
            let p = (i - 1) / 2
            if (keys[p] <= keys[i]) {
                break
            }
            let tk = keys[p]
            keys[p] = keys[i]
            keys[i] = tk
            let ti = ids[p]
            ids[p] = ids[i]
            ids[i] = ti
            i = p
        }
    }

    func pop() {
        let lastKey = keys[keys.size - 1]
        let lastId = ids[ids.size - 1]
        keys.remove(at: keys.size - 1)
        ids.remove(at: ids.size - 1)
        if (keys.size > 0) {
            keys[0] = lastKey
            ids[0] = lastId
            var i: Int64 = 0
            while (true) {
                let l = 2 * i + 1
                let r = 2 * i + 2
                var m = i
                if (l < keys.size && keys[l] < keys[m]) {
                    m = l
                }
                if (r < keys.size && keys[r] < keys[m]) {
                    m = r
                }
                if (m == i) {
                    break
                }
                let tk = keys[m]
                keys[m] = keys[i]
                keys[i] = tk
                let ti = ids[m]
                ids[m] = ids[i]
                ids[i] = ti
                i = m
            }
        }
    }
}

func solve(n: Int64, m: Int64, e: Array<Array<Int64>>): Int64 {
    let head = Array<Int64>(n + 1, repeat: -1)
    let nxt = Array<Int64>(2 * m, repeat: -1)
    let to = Array<Int64>(2 * m, repeat: 0)
    let wt = Array<Int64>(2 * m, repeat: 0)
    var i: Int64 = 0
    while (i < m) {
        let u = e[i][0]
        let v = e[i][1]
        let w = e[i][2]
        to[2 * i] = v
        wt[2 * i] = w
        nxt[2 * i] = head[u]
        head[u] = 2 * i
        to[2 * i + 1] = u
        wt[2 * i + 1] = w
        nxt[2 * i + 1] = head[v]
        head[v] = 2 * i + 1
        i += 1
    }
    let INF: Int64 = 1 << 62
    let d1 = Array<Int64>(n + 1, repeat: INF)
    let d2 = Array<Int64>(n + 1, repeat: INF)
    d1[1] = 0
    let heap = MinHeap()
    heap.push(0, 1)
    while (heap.size() > 0) {
        let d = heap.topKey()
        let u = heap.topId()
        heap.pop()
        if (d <= d2[u]) {
            var k = head[u]
            while (k != -1) {
                let v = to[k]
                let nd = d + wt[k]
                if (nd < d1[v]) {
                    d2[v] = d1[v]
                    d1[v] = nd
                    heap.push(nd, v)
                } else if (nd > d1[v] && nd < d2[v]) {
                    d2[v] = nd
                    heap.push(nd, v)
                }
                k = nxt[k]
            }
        }
    }
    if (d2[n] >= INF) {
        return -1
    }
    return d2[n]
}
