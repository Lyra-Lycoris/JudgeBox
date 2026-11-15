package t01_combination_lock

func parseCode(text: String): Int64 {
    var value = 0
    for (ch in text.toRuneArray()) {
        value = value * 10 + Int64(UInt32(ch) - UInt32(r'0'))
    }
    return value
}

func solve(start: String, target: String, n: Int64, dead: Array<String>): Int64 {
    let blocked = Array<Bool>(10000, repeat: false)
    for (code in dead) {
        blocked[parseCode(code)] = true
    }
    let begin = parseCode(start)
    let goal = parseCode(target)
    if (blocked[begin] || blocked[goal]) {
        return -1
    }
    if (begin == goal) {
        return 0
    }
    let dist = Array<Int64>(10000, repeat: -1)
    let queue = Array<Int64>(10000, repeat: 0)
    var head = 0
    var tail = 0
    dist[begin] = 0
    queue[tail] = begin
    tail += 1
    let power = [1, 10, 100, 1000]
    while (head < tail) {
        let cur = queue[head]
        head += 1
        let step = dist[cur] + 1
        for (p in power) {
            let digit = (cur / p) % 10
            for (nd in [(digit + 1) % 10, (digit + 9) % 10]) {
                let nxt = cur + (nd - digit) * p
                if (dist[nxt] == -1 && !blocked[nxt]) {
                    dist[nxt] = step
                    if (nxt == goal) {
                        return step
                    }
                    queue[tail] = nxt
                    tail += 1
                }
            }
        }
    }
    return -1
}
