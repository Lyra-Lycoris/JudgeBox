package proto_words

func solve(k: Int64, w: Array<String>): Bool {
    for (i in 1..k) {
        if (w[i] != w[0]) {
            return false
        }
    }
    return true
}
