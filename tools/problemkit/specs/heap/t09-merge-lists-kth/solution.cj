package t09_merge_lists_kth

import std.collection.*

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

func solve(k: Int64, m: Int64, t: Int64, lists: Array<Array<Int64>>): Int64 {
    let heap = MinHeap()
    for (r in 0..k) {
        heap.push((lists[r][0] + 1000000000) * 1000000 + r * m)
    }
    var answer = 0
    for (_ in 0..t) {
        let key = heap.pop()
        let code = key % 1000000
        answer = key / 1000000 - 1000000000
        let r = code / m
        let c = code - r * m
        if (c + 1 < m) {
            heap.push((lists[r][c + 1] + 1000000000) * 1000000 + r * m + c + 1)
        }
    }
    return answer
}
