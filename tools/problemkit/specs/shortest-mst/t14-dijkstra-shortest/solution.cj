package t14_dijkstra_shortest

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

func solve(n: Int64, m: Int64, s: Int64, e: Array<Array<Int64>>): Array<Int64> {
    let head = Array<Int64>(n + 1, repeat: -1)
    let nxt = Array<Int64>(m, repeat: -1)
    let to = Array<Int64>(m, repeat: 0)
    let wt = Array<Int64>(m, repeat: 0)
    var i: Int64 = 0
    while (i < m) {
        let u = e[i][0]
        to[i] = e[i][1]
        wt[i] = e[i][2]
        nxt[i] = head[u]
        head[u] = i
        i += 1
    }
    let INF: Int64 = 1 << 62
    let dist = Array<Int64>(n + 1, repeat: INF)
    dist[s] = 0
    let heap = MinHeap()
    heap.push(0, s)
    while (heap.size() > 0) {
        let d = heap.topKey()
        let u = heap.topId()
        heap.pop()
        if (d != dist[u]) {
            continue
        }
        var k = head[u]
        while (k != -1) {
            let v = to[k]
            let nd = d + wt[k]
            if (nd < dist[v]) {
                dist[v] = nd
                heap.push(nd, v)
            }
            k = nxt[k]
        }
    }
    let answer = Array<Int64>(n, repeat: 0)
    var idx: Int64 = 0
    while (idx < n) {
        let v = idx + 1
        if (dist[v] >= INF) {
            answer[idx] = -1
        } else {
            answer[idx] = dist[v]
        }
        idx += 1
    }
    return answer
}
