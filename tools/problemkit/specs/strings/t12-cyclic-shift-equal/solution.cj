package t12_cyclic_shift_equal

func solve(n: Int64, s: String, t: String): Bool {
    let charsS = s.toRuneArray()
    let charsT = t.toRuneArray()
    let m = charsS.size
    if (m != charsT.size) {
        return false
    }
    let doubled = Array<Rune>(2 * m, repeat: r'a')
    for (i in 0..m) {
        doubled[i] = charsS[i]
        doubled[i + m] = charsS[i]
    }
    let bases: Array<Int64> = [131, 137]
    let mods: Array<Int64> = [1000000007, 1000000009]
    for (k in 0..2) {
        let base = bases[k]
        let mod = mods[k]
        var power: Int64 = 1
        for (i in 0..m) {
            power = power * base % mod
        }
        var target: Int64 = 0
        for (i in 0..m) {
            target = (target * base + Int64(UInt32(charsT[i]))) % mod
        }
        let prefix = Array<Int64>(2 * m + 1, repeat: 0)
        for (i in 0..(2 * m)) {
            prefix[i + 1] = (prefix[i] * base + Int64(UInt32(doubled[i]))) % mod
        }
        var matched = false
        for (i in 0..m) {
            let value = (prefix[i + m] - prefix[i] * power % mod + mod) % mod
            if (value == target) {
                matched = true
                break
            }
        }
        if (!matched) {
            return false
        }
    }
    return true
}
