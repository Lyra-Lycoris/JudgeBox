package t09_top_k_frequent

import std.collection.*
import std.sort.*

class NodeHeap {
    var keys: ArrayList<Int64> = ArrayList<Int64>()
    var ids: ArrayList<Int64> = ArrayList<Int64>()

    init() {}

    func size(): Int64 {
        return ids.size
    }

    func topKey(): Int64 {
        return keys[0]
    }

    func push(key: Int64, id: Int64) {
        keys.add(key)
        ids.add(id)
        var i = ids.size - 1
        while (i > 0) {
            let p = (i - 1) / 2
            if (keys[p] < keys[i] || (keys[p] == keys[i] && ids[p] <= ids[i])) {
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

    func popId(): Int64 {
        let first = ids[0]
        let lastKey = keys[keys.size - 1]
        let lastId = ids[ids.size - 1]
        keys.remove(at: keys.size - 1)
        ids.remove(at: ids.size - 1)
        if (ids.size > 0) {
            keys[0] = lastKey
            ids[0] = lastId
            var i = 0
            while (true) {
                let l = 2 * i + 1
                let r = 2 * i + 2
                var m = i
                if (l < ids.size && (keys[l] < keys[m] || (keys[l] == keys[m] && ids[l] < ids[m]))) {
                    m = l
                }
                if (r < ids.size && (keys[r] < keys[m] || (keys[r] == keys[m] && ids[r] < ids[m]))) {
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
        return first
    }
}

func solve(n: Int64, k: Int64, a: Array<Int64>): Array<Int64> {
    let sorted = a.clone()
    sort(sorted)
    let heap = NodeHeap()
    var i = 0
    while (i < n) {
        var j = i
        while (j < n && sorted[j] == sorted[i]) {
            j += 1
        }
        heap.push(-(j - i), sorted[i])
        i = j
    }
    let answer = Array<Int64>(k, repeat: 0)
    for (p in 0..k) {
        answer[p] = heap.popId()
    }
    return answer
}
