package t12_longest_common_prefix

func solve(k: Int64, words: Array<String>): Int64 {
    let runes = Array<Array<Rune>>(k, { _ => Array<Rune>(0, repeat: r'a') })
    var limit: Int64 = -1
    for (i in 0..k) {
        let current = words[i].toRuneArray()
        runes[i] = current
        if (limit < 0 || current.size < limit) {
            limit = current.size
        }
    }
    if (limit <= 0) {
        return 0
    }
    var answer: Int64 = 0
    while (answer < limit) {
        let ch = runes[0][answer]
        var ok = true
        for (i in 0..k) {
            if (runes[i][answer] != ch) {
                ok = false
                break
            }
        }
        if (!ok) {
            break
        }
        answer += 1
    }
    return answer
}
