package t25_bracket_depth

func solve(n: Int64, k: Int64): String {
    let bytes = Array<UInt8>(n, repeat: 0)
    var at: Int64 = 0
    var i: Int64 = 0
    while (i < k) {
        bytes[at] = 40
        at += 1
        i += 1
    }
    i = 0
    while (i < k) {
        bytes[at] = 41
        at += 1
        i += 1
    }
    let pairs = (n - 2 * k) / 2
    i = 0
    while (i < pairs) {
        bytes[at] = 40
        at += 1
        bytes[at] = 41
        at += 1
        i += 1
    }
    return String.fromUtf8(bytes)
}
