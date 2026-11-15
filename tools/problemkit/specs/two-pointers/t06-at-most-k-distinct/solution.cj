package t06_at_most_k_distinct

func solve(k: Int64, s: String): Int64 {
    if (k <= 0) {
        return 0
    }
    let chars = s.toRuneArray()
    let total = chars.size
    if (total == 0) {
        return 0
    }
    let count = Array<Int64>(256, repeat: 0)
    var distinct: Int64 = 0
    var best: Int64 = 0
    var left: Int64 = 0
    var right: Int64 = 0
    while (right < total) {
        let c = Int64(UInt32(chars[right]))
        if (count[c] == 0) {
            distinct += 1
        }
        count[c] += 1
        while (distinct > k) {
            let d = Int64(UInt32(chars[left]))
            count[d] -= 1
            if (count[d] == 0) {
                distinct -= 1
            }
            left += 1
        }
        if (right - left + 1 > best) {
            best = right - left + 1
        }
        right += 1
    }
    return best
}
