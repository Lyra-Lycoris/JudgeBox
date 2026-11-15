package t06_longest_unique_substring

func solve(s: String): Int64 {
    let chars = s.toRuneArray()
    let last = Array<Int64>(256, repeat: -1)
    var best: Int64 = 0
    var left: Int64 = 0
    let total = chars.size
    for (right in 0..total) {
        let c = Int64(UInt32(chars[right]))
        if (last[c] >= left) {
            left = last[c] + 1
        }
        last[c] = right
        if (right - left + 1 > best) {
            best = right - left + 1
        }
    }
    return best
}
