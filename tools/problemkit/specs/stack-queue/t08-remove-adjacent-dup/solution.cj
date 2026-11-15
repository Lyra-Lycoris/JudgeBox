package t08_remove_adjacent_dup

func solve(k: Int64, s: String): String {
    let chars = s.toRuneArray()
    let stackCh = Array<Int64>(chars.size + 1, repeat: 0)
    let stackCnt = Array<Int64>(chars.size + 1, repeat: 0)
    var top = 0
    for (ch in chars) {
        let code = Int64(UInt32(ch))
        if (top > 0 && stackCh[top - 1] == code) {
            stackCnt[top - 1] += 1
            if (stackCnt[top - 1] == k) {
                top -= 1
            }
        } else {
            stackCh[top] = code
            stackCnt[top] = 1
            top += 1
        }
    }
    var total = 0
    for (i in 0..top) {
        total += stackCnt[i]
    }
    let bytes = Array<UInt8>(total, repeat: 0)
    var pos = 0
    for (i in 0..top) {
        for (j in 0..stackCnt[i]) {
            bytes[pos] = UInt8(UInt32(stackCh[i]))
            pos += 1
        }
    }
    return String.fromUtf8(bytes)
}
