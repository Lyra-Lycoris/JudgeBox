package t09_meeting_rooms_busiest

import std.collection.*
import std.sort.*

class MinHeap {
    var data: ArrayList<Int64> = ArrayList<Int64>()

    init() {}

    func size(): Int64 {
        return data.size
    }

    func top(): Int64 {
        return data[0]
    }

    func push(x: Int64) {
        data.add(x)
        var i = data.size - 1
        while (i > 0) {
            let p = (i - 1) / 2
            if (data[p] <= data[i]) {
                break
            }
            let t = data[p]
            data[p] = data[i]
            data[i] = t
            i = p
        }
    }

    func pop(): Int64 {
        let first = data[0]
        let last = data[data.size - 1]
        data.remove(at: data.size - 1)
        if (data.size > 0) {
            data[0] = last
            var i = 0
            while (true) {
                let l = 2 * i + 1
                let r = 2 * i + 2
                var m = i
                if (l < data.size && data[l] < data[m]) {
                    m = l
                }
                if (r < data.size && data[r] < data[m]) {
                    m = r
                }
                if (m == i) {
                    break
                }
                let t = data[m]
                data[m] = data[i]
                data[i] = t
                i = m
            }
        }
        return first
    }
}

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

func solve(n: Int64, m: Int64, s: Array<Int64>, d: Array<Int64>): Int64 {
    let order = Array<Int64>(m, repeat: 0)
    for (i in 0..m) {
        order[i] = s[i] * 1000000 + i
    }
    sort(order)
    let free = MinHeap()
    for (i in 0..n) {
        free.push(i)
    }
    let busy = NodeHeap()
    let used = Array<Int64>(n, repeat: 0)
    for (p in 0..m) {
        let key = order[p]
        let idx = key % 1000000
        let start = key / 1000000
        while (busy.size() > 0 && busy.topKey() <= start) {
            let ready = busy.popId()
            free.push(ready)
        }
        var room = 0
        if (free.size() > 0) {
            room = free.pop()
            busy.push(start + d[idx], room)
        } else {
            let finish = busy.topKey()
            room = busy.popId()
            busy.push(finish + d[idx], room)
        }
        used[room] = used[room] + 1
    }
    var best = 0
    for (i in 1..n) {
        if (used[i] > used[best]) {
            best = i
        }
    }
    return best
}
