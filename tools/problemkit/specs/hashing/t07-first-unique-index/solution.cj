package t07_first_unique_index

func solve(n: Int64, s: String): Int64 {
    let counts = Array<Int64>(26, repeat: 0)
    for (ch in s.toRuneArray()) {
        let index = Int64(UInt32(ch) - UInt32(r'a'))
        counts[index] += 1
    }
    var position = 0
    for (ch in s.toRuneArray()) {
        let index = Int64(UInt32(ch) - UInt32(r'a'))
        if (counts[index] == 1) {
            return position + 1
        }
        position += 1
    }
    return -1
}
