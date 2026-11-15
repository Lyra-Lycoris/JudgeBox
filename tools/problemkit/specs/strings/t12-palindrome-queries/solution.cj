package t12_palindrome_queries

func solve(n: Int64, s: String, q: Int64, qs: Array<Array<Int64>>): Array<Int64> {
    let chars = s.toRuneArray()
    let m = chars.size
    let answer = Array<Int64>(q, repeat: 1)
    let bases: Array<Int64> = [131, 137]
    let mods: Array<Int64> = [1000000007, 1000000009]
    for (k in 0..2) {
        let base = bases[k]
        let mod = mods[k]
        let power = Array<Int64>(m + 1, repeat: 1)
        for (i in 0..m) {
            power[i + 1] = power[i] * base % mod
        }
        let forwardHash = Array<Int64>(m + 1, repeat: 0)
        let reverseHash = Array<Int64>(m + 1, repeat: 0)
        for (i in 0..m) {
            forwardHash[i + 1] = (forwardHash[i] * base + Int64(UInt32(chars[i]))) % mod
            reverseHash[i + 1] = (reverseHash[i] * base + Int64(UInt32(chars[m - 1 - i]))) % mod
        }
        for (j in 0..q) {
            let left = qs[j][0] - 1
            let right = qs[j][1]
            let length = right - left
            let direct = (forwardHash[right] - forwardHash[left] * power[length] % mod + mod) % mod
            let mirrored = (reverseHash[m - left] - reverseHash[m - right] * power[length] % mod + mod) % mod
            if (direct != mirrored) {
                answer[j] = 0
            }
        }
    }
    return answer
}
