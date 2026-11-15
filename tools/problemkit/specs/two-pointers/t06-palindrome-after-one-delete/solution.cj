package t06_palindrome_after_one_delete

func isPalindromeRange(chars: Array<Rune>, start: Int64, finish: Int64): Bool {
    var left = start
    var right = finish
    while (left < right) {
        if (chars[left] != chars[right]) {
            return false
        }
        left += 1
        right -= 1
    }
    return true
}

func solve(s: String): Bool {
    let chars = s.toRuneArray()
    var left: Int64 = 0
    var right: Int64 = chars.size - 1
    while (left < right) {
        if (chars[left] == chars[right]) {
            left += 1
            right -= 1
        } else {
            return isPalindromeRange(chars, left + 1, right) || isPalindromeRange(chars, left, right - 1)
        }
    }
    return true
}
