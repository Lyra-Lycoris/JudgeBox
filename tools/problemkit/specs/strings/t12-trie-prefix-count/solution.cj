package t12_trie_prefix_count

func solve(n: Int64, words: Array<String>, q: Int64, queries: Array<String>): Array<Int64> {
    var total: Int64 = 0
    for (w in words) {
        total += w.size
    }
    let capacity = total + 2
    let child = Array<Int64>(capacity * 26, repeat: 0)
    let passing = Array<Int64>(capacity, repeat: 0)
    var used: Int64 = 0
    for (w in words) {
        var current: Int64 = 0
        for (ch in w.toRuneArray()) {
            let key = current * 26 + Int64(UInt32(ch) - UInt32(r'a'))
            if (child[key] == 0) {
                used += 1
                child[key] = used
            }
            current = child[key]
            passing[current] += 1
        }
    }
    let answer = Array<Int64>(q, repeat: 0)
    for (j in 0..q) {
        var current: Int64 = 0
        var found = true
        for (ch in queries[j].toRuneArray()) {
            let nxt = child[current * 26 + Int64(UInt32(ch) - UInt32(r'a'))]
            if (nxt == 0) {
                found = false
                break
            }
            current = nxt
        }
        if (found) {
            answer[j] = passing[current]
        }
    }
    return answer
}
