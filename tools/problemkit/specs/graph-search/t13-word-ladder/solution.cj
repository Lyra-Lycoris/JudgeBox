package t13_word_ladder

import std.collection.*

func __t13Pattern(word: String, skip: Int64): String {
    let runes = word.toRuneArray()
    let sb = StringBuilder()
    for (i in 0..runes.size) {
        if (i == skip) {
            sb.append("*")
        } else {
            sb.append(runes[i].toString())
        }
    }
    return sb.toString()
}

func solve(n: Int64, begin: String, end: String, w: Array<String>): Int64 {
    if (begin == end) {
        return 1
    }
    var target: Int64 = -1
    var bidx: Int64 = -1
    for (i in 0..n) {
        if (target == -1 && w[i] == end) {
            target = i
        }
        if (bidx == -1 && w[i] == begin) {
            bidx = i
        }
    }
    if (target == -1) {
        return 0
    }
    let buckets = HashMap<String, ArrayList<Int64>>()
    for (i in 0..n) {
        let width = w[i].toRuneArray().size
        for (j in 0..width) {
            let key = __t13Pattern(w[i], j)
            if (buckets.contains(key)) {
                buckets[key].add(i)
            } else {
                let group = ArrayList<Int64>()
                group.add(i)
                buckets[key] = group
            }
        }
    }
    let dist = Array<Int64>(n + 1, repeat: -1)
    dist[n] = 1
    if (bidx != -1) {
        dist[bidx] = 1
    }
    let queue = Array<Int64>(n + 1, repeat: 0)
    var head: Int64 = 0
    var tail: Int64 = 0
    queue[tail] = n
    tail += 1
    while (head < tail) {
        let u = queue[head]
        head += 1
        let step = dist[u] + 1
        var word = begin
        if (u != n) {
            word = w[u]
        }
        let width = word.toRuneArray().size
        for (j in 0..width) {
            let key = __t13Pattern(word, j)
            if (!buckets.contains(key)) {
                continue
            }
            let group = buckets[key]
            buckets.remove(key)
            for (v in group) {
                if (dist[v] != -1) {
                    continue
                }
                dist[v] = step
                if (v == target) {
                    return step
                }
                queue[tail] = v
                tail += 1
            }
        }
    }
    return 0
}
